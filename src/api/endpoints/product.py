from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ...core.database import get_db
from ...models.product import ProductPrd
import logging

logger = logging.getLogger(__name__)

router = APIRouter()

@router.get("/products")
async def search_product(code: str, db: Session = Depends(get_db)):
    logger.debug(f"Searching for product with code: {code}")
    try:
        # クエリをログ出力
        query = db.query(ProductPrd).filter(ProductPrd.CODE == code)
        logger.debug(f"SQL Query: {query}")
        
        product = query.first()
        
        if product:
            logger.debug(f"Found product: {product.NAME}, {product.PRICE}")
            return {
                "code": product.CODE,
                "name": product.NAME,
                "price": product.PRICE
            }
        else:
            logger.debug(f"No product found for code: {code}")
            return {
                "code": code,
                "name": "商品がマスタ未登録です",
                "price": None
            }
            
    except Exception as e:
        logger.error(f"Database error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
        