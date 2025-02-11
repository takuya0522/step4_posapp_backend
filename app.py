from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import text
from src.core.database import engine
from pydantic import BaseModel
from typing import List
import logging
from src.api.routes import router  # 既存のルーターをインポート

# リクエストボディ用のモデルを定義
class TransactionItem(BaseModel):
    code: str
    name: str
    price: int

class TransactionRequest(BaseModel):
    items: List[TransactionItem]

app = FastAPI()

# CORSの設定を修正
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://tech0-gen8-step4-pos-app-85.azurewebsites.net",
        "http://localhost:3000",
        "http://127.0.0.1:3000"  # これを追加
    ],
    allow_credentials=False,  # Trueから変更
    allow_methods=["*"],
    allow_headers=["*"]
)

# 商品検索のエンドポイント
@app.get("/api/products/lookup/{code}")
async def lookup_product(code: str):
    with engine.connect() as connection:
        query = text("SELECT * FROM m_product_yama_prd WHERE CODE = :code")
        result = connection.execute(query, {"code": code}).first()
        
        if result is None:
            raise HTTPException(status_code=404, detail="商品が見つかりませんでした")
            
        return {
            "code": result.CODE.strip(),
            "name": result.NAME,
            "price": result.PRICE
        }

@app.post("/api/transactions")
async def create_transaction(request: TransactionRequest):
    try:
        with engine.connect() as connection:
            # トランザクション開始
            with connection.begin():
                # トランザクションヘッダを登録
                header_query = text("""
                    INSERT INTO m_product_yama_trd 
                    (DATETIME, EMP_CD, STORE_CD, POS_NO, TOTAL_AMT) 
                    VALUES (NOW(), 'E001', 'S001', 'P01', :total_amount)
                """)
                
                # 合計金額を計算
                total_amount = sum(item.price for item in request.items)
                
                # トランザクションヘッダを挿入
                result = connection.execute(header_query, {
                    "total_amount": total_amount
                })
                
                # 最後に挿入されたIDを取得
                get_id_query = text("SELECT LAST_INSERT_ID()")
                trd_id = connection.execute(get_id_query).scalar()

                # トランザクション明細を登録
                for item in request.items:
                    detail_query = text("""
                        INSERT INTO m_product_yama_dtl 
                        (TRD_ID, PRD_CODE, PRD_NAME, PRD_PRICE)
                        VALUES (:trd_id, :code, :name, :price)
                    """)
                    connection.execute(detail_query, {
                        "trd_id": trd_id,
                        "code": item.code,
                        "name": item.name,
                        "price": item.price
                    })
                    logger.debug(f"Added item {item.code} to transaction {trd_id}")

                return {
                    "message": "Transaction created successfully",
                    "transaction_id": trd_id,
                    "total_amount": total_amount
                }
                
    except Exception as e:
        logger.error(f"Error creating transaction: {str(e)}")
        raise HTTPException(
            status_code=500, 
            detail=f"Database error: {str(e)}"
        )

# 既存のルーターを使用
app.include_router(router)