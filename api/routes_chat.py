from fastapi import APIRouter, Request, UploadFile, File, Form, HTTPException
from schemas.chat import AskTextRequest
from services.pipeline import ask_text, ask_audio, ask_audio_with_tts

router = APIRouter(prefix="/api/v1/chat", tags=["chat"])


@router.post("/text")
async def chat_text(payload: AskTextRequest, request: Request):
    try:
        result = await ask_text(
            config=request.app.state.config,
            modules=request.app.state.modules,
            dialogues_store=request.app.state.dialogues,
            text=payload.text,
            session_id=payload.session_id,
        )
        return {
            "code": 0,
            "message": "success",
            "data": result,
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/audio")
async def chat_audio(
    request: Request,
    file: UploadFile = File(...),
    session_id: str | None = Form(default=None),
):
    try:
        file_bytes = await file.read()
        result = await ask_audio(
            config=request.app.state.config,
            modules=request.app.state.modules,
            dialogues_store=request.app.state.dialogues,
            file_bytes=file_bytes,
            filename=file.filename or "audio.wav",
            session_id=session_id,
        )
        return {
            "code": 0,
            "message": "success",
            "data": result,
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/audio-tts")
async def chat_audio_tts(
    request: Request,
    file: UploadFile = File(...),
    session_id: str | None = Form(default=None),
):
    try:
        file_bytes = await file.read()
        result = await ask_audio_with_tts(
            config=request.app.state.config,
            modules=request.app.state.modules,
            dialogues_store=request.app.state.dialogues,
            file_bytes=file_bytes,
            filename=file.filename or "audio.wav",
            session_id=session_id,
        )
        return {
            "code": 0,
            "message": "success",
            "data": result,
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))