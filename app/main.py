from fastapi import FastAPI, Depends  # ✅ Depends to'g'ri joyga ko'chirildi
from app.api import frontend_routes   # ✅ frontend_routes alohida import qilingan
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from starlette.middleware.base import BaseHTTPMiddleware
import logging
import time
from typing import Callable
import asyncio
from contextlib import asynccontextmanager

from app.api.api import api_router
from app.core.config import settings
from app.api.websockets import start_background_tasks

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)


class LoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        start_time = time.time()
        response = await call_next(request)
        process_time = time.time() - start_time
        logger.info(f"{request.method} {request.url.path} - {response.status_code} - {process_time:.4f}s")
        return response


@asynccontextmanager
async def lifespan(app: FastAPI):
    await start_background_tasks()
    yield


app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    lifespan=lifespan
)

# CORS
if settings.BACKEND_CORS_ORIGINS:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[str(origin) for origin in settings.BACKEND_CORS_ORIGINS],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

# Middlewares
app.add_middleware(LoggingMiddleware)

# Routers
app.include_router(api_router, prefix=settings.API_V1_STR)
app.include_router(frontend_routes.router)  # ✅ frontend sahifalar uchun marshrutlar

# Root route
@app.get("/")
def root():
    return {"message": "Bog'cha oshxona tizimi API. /docs sahifasiga o'ting."}


if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
