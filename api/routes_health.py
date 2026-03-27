from fastapi import APIRouter, Request

router = APIRouter(tags=["health"])


@router.get("/health")
async def health(request: Request):
    modules = getattr(request.app.state, "modules", {})
    config = getattr(request.app.state, "config", {})

    return {
        "code": 0,
        "message": "success",
        "data": {
            "status": "ok",
            "loaded_modules": list(modules.keys()),
            "selected_module": config.get("selected_module", {}),
        },
    }