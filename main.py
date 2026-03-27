import os

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from config.config_loader import load_config
from services.module_loader import init_all_modules
from api.routes_health import router as health_router
from api.routes_chat import router as chat_router


app = FastAPI(
    title="QA Service",
    version="0.1.0",
    description="阶段三独立问答服务：文本问答、语音问答、语音问答+TTS",
)

os.makedirs("tmp", exist_ok=True)
os.makedirs("data", exist_ok=True)

app.mount("/static", StaticFiles(directory="tmp"), name="static")

app.include_router(health_router)
app.include_router(chat_router)


@app.on_event("startup")
async def startup_event():
    config = load_config()
    modules = init_all_modules(config)

    app.state.config = config
    app.state.modules = modules
    app.state.dialogues = {}


@app.get("/")
async def root():
    return {
        "code": 0,
        "message": "success",
        "data": {
            "name": "qa-service",
            "docs": "/docs",
            "health": "/health",
        },
    }