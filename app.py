from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import text
import logging
from src.core.database import engine

# ログ設定を追加
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

app = FastAPI()

# CORSの設定
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://tech0-gen8-step4-pos-app-85.azurewebsites.net",
        "http://localhost:3000"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

# データベース接続テスト用エンドポイント
@app.get("/api/test-db")
async def test_db():
    try:
        with engine.connect() as connection:
            result = connection.execute(text("SELECT 1"))
            return {"status": "success", "message": "Database connection successful"}
    except Exception as e:
        logger.error(f"Database connection error: {str(e)}")
        return {"status": "error", "message": str(e)}

# 商品検索のエンドポイント
@app.get("/api/products/lookup/{code}")
async def lookup_product(code: str):
    try:
        logger.debug(f"Attempting to connect to database")
        with engine.connect() as connection:
            logger.debug(f"Database connection successful")
            query = text("SELECT * FROM m_product_yama_prd WHERE code = :code")
            logger.debug(f"Executing query: {query}")
            result = connection.execute(query, {"code": code}).first()
            logger.debug(f"Query executed, result: {result}")
            
            if result is None:
                return {"detail": "Not Found"}
                
            return {
                "id": result.PRD_ID,
                "code": result.CODE.strip(),
                "name": result.NAME,
                "price": result.PRICE
            }
    except Exception as e:
        logger.error(f"Error details: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))