from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from urllib.parse import quote_plus

# MySQL接続情報
DB_HOST = "tech0-gen-8-step4-db-4.mysql.database.azure.com"
DB_USER = "Tech0Gen8TA4"
DB_PASSWORD = quote_plus("gen8-1-ta@4")
DB_NAME = "db_class4"

DATABASE_URL = f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:3306/{DB_NAME}"

engine = create_engine(
    DATABASE_URL,
    echo=True,
    connect_args={
        "ssl": {
            "ssl_mode": "REQUIRED",
            "ssl": True
        }
    }
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
