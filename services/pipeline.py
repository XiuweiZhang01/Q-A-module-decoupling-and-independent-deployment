import os
import uuid
import asyncio
from typing import Dict, Any, Optional

from core.utils.dialogue import Dialogue, Message
from services.audio_convert import audio_file_to_pcm_chunks


def _build_system_prompt(config: Dict[str, Any]) -> str:
    prompt = config.get("prompt")
    if isinstance(prompt, str) and prompt.strip():
        return prompt
    return "你是一个有帮助的中文语音助手，请简洁、自然、准确地回答问题。"


def _get_or_create_dialogue(
    dialogues_store: Dict[str, Dialogue],
    session_id: str,
    system_prompt: str,
) -> Dialogue:
    dialogue = dialogues_store.get(session_id)
    if dialogue is None:
        dialogue = Dialogue()
        dialogue.update_system_message(system_prompt)
        dialogues_store[session_id] = dialogue
        return dialogue

    has_system = any(msg.role == "system" for msg in dialogue.dialogue)
    if not has_system:
        dialogue.update_system_message(system_prompt)

    return dialogue


def _collect_llm_response_sync(llm_instance, session_id: str, llm_dialogue) -> str:
    """
    LLMProvider.response(...) 是同步生成器，这里在同步线程里把它收集成完整字符串。
    """
    chunks = []
    for piece in llm_instance.response(session_id, llm_dialogue):
        if piece:
            chunks.append(piece)
    return "".join(chunks).strip()


async def ask_text(
    config: Dict[str, Any],
    modules: Dict[str, Any],
    dialogues_store: Dict[str, Dialogue],
    text: str,
    session_id: Optional[str] = None,
) -> Dict[str, Any]:
    if not text or not text.strip():
        raise ValueError("text 不能为空")

    if not session_id:
        session_id = uuid.uuid4().hex

    llm_instance = modules["llm"]
    system_prompt = _build_system_prompt(config)
    dialogue = _get_or_create_dialogue(dialogues_store, session_id, system_prompt)

    user_text = text.strip()
    dialogue.put(Message(role="user", content=user_text))

    llm_dialogue = dialogue.get_llm_dialogue()

    answer_text = await asyncio.to_thread(
        _collect_llm_response_sync,
        llm_instance,
        session_id,
        llm_dialogue,
    )

    if not answer_text:
        answer_text = "抱歉，我刚刚没有成功生成回答，请再试一次。"

    dialogue.put(Message(role="assistant", content=answer_text))
    dialogue.trim_history(max_turns=10)

    return {
        "session_id": session_id,
        "input_text": user_text,
        "answer_text": answer_text,
    }


async def ask_audio(
    config: Dict[str, Any],
    modules: Dict[str, Any],
    dialogues_store: Dict[str, Dialogue],
    file_bytes: bytes,
    filename: str,
    session_id: Optional[str] = None,
) -> Dict[str, Any]:
    if not file_bytes:
        raise ValueError("上传文件为空")

    if not session_id:
        session_id = uuid.uuid4().hex

    asr_instance = modules["asr"]

    suffix = os.path.splitext(filename or "")[1] or ".wav"
    pcm_chunks = audio_file_to_pcm_chunks(file_bytes, suffix=suffix, work_dir="tmp")

    raw_text, _ = await asr_instance.speech_to_text_wrapper(
        pcm_chunks,
        session_id,
        audio_format="pcm",
    )

    if isinstance(raw_text, dict):
        asr_text = (raw_text.get("content") or "").strip()
    elif raw_text is None:
        asr_text = ""
    else:
        asr_text = str(raw_text).strip()

    if not asr_text:
        raise RuntimeError("ASR 没有识别出有效文本，请更换更清晰的音频重试。")

    text_result = await ask_text(
        config=config,
        modules=modules,
        dialogues_store=dialogues_store,
        text=asr_text,
        session_id=session_id,
    )

    return {
        "session_id": text_result["session_id"],
        "asr_text": asr_text,
        "answer_text": text_result["answer_text"],
    }


async def ask_audio_with_tts(
    config: Dict[str, Any],
    modules: Dict[str, Any],
    dialogues_store: Dict[str, Dialogue],
    file_bytes: bytes,
    filename: str,
    session_id: Optional[str] = None,
) -> Dict[str, Any]:
    audio_result = await ask_audio(
        config=config,
        modules=modules,
        dialogues_store=dialogues_store,
        file_bytes=file_bytes,
        filename=filename,
        session_id=session_id,
    )

    tts_instance = modules["tts"]
    answer_text = audio_result["answer_text"]

    os.makedirs("tmp", exist_ok=True)

    # 不调用 tts.to_tts()，因为它内部用了 asyncio.run，
    # 在 FastAPI 的异步接口里会报错。
    output_ext = "." + getattr(tts_instance, "audio_file_type", "mp3").lstrip(".")
    output_path = tts_instance.generate_filename(extension=output_ext)

    await tts_instance.text_to_speak(answer_text, output_path)

    if not os.path.exists(output_path):
        raise RuntimeError("TTS 执行完成，但没有生成音频文件。")

    audio_result["audio_url"] = f"/static/{os.path.basename(output_path)}"
    audio_result["audio_file"] = output_path
    return audio_result