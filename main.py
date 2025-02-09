import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.api.routes import router
import logging
import os

# ロギングの設定を詳細にする
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

app = FastAPI()

@app.on_event("startup")
async def startup_event():
    logger.debug("Starting up FastAPI application...")

# CORSの設定
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 本番環境では適切なオリジンに制限してください
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# リクエストをログ出力するミドルウェア
@app.middleware("http")
async def log_requests(request, call_next):
    logger.debug(f"Incoming request: {request.method} {request.url}")
    response = await call_next(request)
    return response

# ルーターを追加する前にログを出力
logger.debug("Registering routes...")
app.include_router(router)

@app.get("/api/health")
async def health_check():
    logger.debug("Health check endpoint called")
    return {"status": "ok"}

# デバッグ用のルートを追加
@app.get("/")
async def root():
    return {"message": "API is running"}

if __name__ == "__main__":
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=port,
        reload=False  # 本番環境ではFalse
    )