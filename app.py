from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

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

# 商品検索のエンドポイント
@app.get("/api/products/lookup/{code}")
async def lookup_product(code: str):
    query = text("SELECT * FROM m_product_yama_prd WHERE code = :code")
    # ...