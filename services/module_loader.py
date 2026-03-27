from typing import Dict, Any

from config.logger import setup_logging
from core.utils import vad, asr, llm, tts

TAG = __name__
logger = setup_logging()


def _get_delete_audio_flag(config: Dict[str, Any]) -> bool:
    return str(config.get("delete_audio", True)).lower() in ("true", "1", "yes")


def init_vad(config: Dict[str, Any]):
    selected_name = config["selected_module"]["VAD"]
    provider_config = config["VAD"][selected_name]
    provider_type = provider_config.get("type", selected_name)

    instance = vad.create_instance(provider_type, provider_config)
    logger.bind(tag=TAG).info(f"初始化组件: vad 成功 -> {selected_name} ({provider_type})")
    return instance


def init_asr(config: Dict[str, Any]):
    selected_name = config["selected_module"]["ASR"]
    provider_config = config["ASR"][selected_name]
    provider_type = provider_config.get("type", selected_name)
    delete_audio = _get_delete_audio_flag(config)

    instance = asr.create_instance(provider_type, provider_config, delete_audio)
    logger.bind(tag=TAG).info(f"初始化组件: asr 成功 -> {selected_name} ({provider_type})")
    return instance


def init_llm(config: Dict[str, Any]):
    selected_name = config["selected_module"]["LLM"]
    provider_config = config["LLM"][selected_name]
    provider_type = provider_config.get("type", selected_name)

    instance = llm.create_instance(provider_type, provider_config)
    logger.bind(tag=TAG).info(f"初始化组件: llm 成功 -> {selected_name} ({provider_type})")
    return instance


def init_tts(config: Dict[str, Any]):
    selected_name = config["selected_module"]["TTS"]
    provider_config = config["TTS"][selected_name]
    provider_type = provider_config.get("type", selected_name)
    delete_audio = _get_delete_audio_flag(config)

    instance = tts.create_instance(provider_type, provider_config, delete_audio)
    logger.bind(tag=TAG).info(f"初始化组件: tts 成功 -> {selected_name} ({provider_type})")
    return instance


def init_all_modules(config: Dict[str, Any]) -> Dict[str, Any]:
    modules = {
        "vad": init_vad(config),
        "asr": init_asr(config),
        "llm": init_llm(config),
        "tts": init_tts(config),
    }
    logger.bind(tag=TAG).info("四个核心模块初始化完成")
    return modules