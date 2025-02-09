from sqlalchemy import Column, String, Integer
from ..core.database import Base

class ProductPrd(Base):
    __tablename__ = "m_product_yama_prd"

    PRD_ID = Column(Integer, primary_key=True, autoincrement=True)
    CODE = Column(String(13))
    NAME = Column(String(50))
    PRICE = Column(Integer)

    def __repr__(self):
        return f"<Product(CODE='{self.CODE}', NAME='{self.NAME}', PRICE={self.PRICE})>"
