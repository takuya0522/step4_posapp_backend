from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import logging
from urllib.parse import quote_plus

logger = logging.getLogger(__name__)

# Azure MySQL接続情報
DB_HOST = "tech0-gen-8-step4-db-4.mysql.database.azure.com"
DB_USER = "Tech0Gen8TA4"
DB_PASSWORD = quote_plus("gen8-1-ta@4")
DB_NAME = "db_class4"

# SSL要求を追加したconnect_args
DATABASE_URL = f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:3306/{DB_NAME}"

try:
    engine = create_engine(
        DATABASE_URL,
        echo=True,
        connect_args={
            "ssl": {
                "ssl_mode": "VERIFY_IDENTITY",
                "ssl": True
            }
        }
    )
    logger.debug("Database connection established")
except Exception as e:
    logger.error(f"Database connection failed: {str(e)}")

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        logger.debug("Database session created")
        yield db
    finally:
        logger.debug("Database session closed")
        db.close()
