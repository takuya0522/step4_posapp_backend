from pydantic import BaseModel
from typing import List
from datetime import datetime

class TransactionItemCreate(BaseModel):
    code: str
    name: str
    price: int

class TransactionCreate(BaseModel):
    items: List[TransactionItemCreate]
    emp_cd: str = "0001"  # デフォルト値
    store_cd: str = "00001"  # デフォルト値
    pos_no: str = "001"  # デフォルト値

class TransactionResponse(BaseModel):
    success: bool
    message: str
    transaction_id: int
    total: int
