from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ...core.database import get_db
from ...models.transaction import Transaction, TransactionDetail
from ...models.product import ProductPrd  # 商品マスタモデルをインポート
from ...schemas.transaction import TransactionCreate, TransactionResponse
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

router = APIRouter()

@router.post("/transactions", response_model=TransactionResponse)
async def create_transaction(transaction: TransactionCreate, db: Session = Depends(get_db)):
    try:
        logger.debug(f"Received transaction request with {len(transaction.items)} items")
        
        # 合計金額を計算
        total_amount = sum(item.price for item in transaction.items)

        # トランザクションヘッダーを作成
        db_transaction = Transaction(
            DATETIME = datetime.now(),
            EMP_CD = "E001",
            STORE_CD = "S001",
            POS_NO = "P01",
            TOTAL_AMT = total_amount
        )
        db.add(db_transaction)
        db.flush()
        
        logger.debug(f"Created transaction header with ID: {db_transaction.TRD_ID}")

        # トランザクション明細を作成
        for item in transaction.items:
            # 商品マスタから商品情報を取得
            product = db.query(ProductPrd).filter(ProductPrd.CODE == item.code).first()
            if not product:
                raise HTTPException(status_code=404, detail=f"商品コード {item.code} が見つかりません")

            detail = TransactionDetail(
                TRD_ID = db_transaction.TRD_ID,
                PRD_ID = product.PRD_ID,  # 商品マスタから取得したPRD_IDを設定
                PRD_CODE = item.code,
                PRD_NAME = item.name,
                PRD_PRICE = item.price
            )
            db.add(detail)
            logger.debug(f"Added detail for product: {item.code} with PRD_ID: {product.PRD_ID}")

        db.commit()
        logger.debug(f"Transaction committed successfully")
        
        return TransactionResponse(
            success=True,
            message="取引が完了しました",
            transaction_id=db_transaction.TRD_ID,
            total=total_amount
        )
    except Exception as e:
        db.rollback()
        logger.error(f"Error creating transaction: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
