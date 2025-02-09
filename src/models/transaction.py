from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from ..core.database import Base
from datetime import datetime

class Transaction(Base):
    __tablename__ = "m_product_yama_trd"

    TRD_ID = Column(Integer, primary_key=True, autoincrement=True)
    DATETIME = Column(DateTime, default=datetime.now)
    EMP_CD = Column(String(10), default="E001")
    STORE_CD = Column(String(5), default="S001")
    POS_NO = Column(String(3), default="P01")
    TOTAL_AMT = Column(Integer)

class TransactionDetail(Base):
    __tablename__ = "m_product_yama_dtl"

    DTL_ID = Column(Integer, primary_key=True, autoincrement=True)  # シーケンス定義を単純化
    TRD_ID = Column(Integer, ForeignKey("m_product_yama_trd.TRD_ID"))
    PRD_ID = Column(Integer, nullable=False)
    PRD_CODE = Column(String(13), nullable=False)
    PRD_NAME = Column(String(50), nullable=False)
    PRD_PRICE = Column(Integer, nullable=False)

    def __repr__(self):
        return f"<TransactionDetail(DTL_ID={self.DTL_ID}, TRD_ID={self.TRD_ID}, PRD_CODE={self.PRD_CODE})>"
