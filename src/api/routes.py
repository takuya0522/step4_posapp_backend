from fastapi import APIRouter
from .endpoints import product, transaction

router = APIRouter()

# 各エンドポイントのルーターをインクルード
router.include_router(product.router, prefix="/api", tags=["products"])
router.include_router(transaction.router, prefix="/api", tags=["transactions"])
