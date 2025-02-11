from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# CORS設定を追加
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://tech0-gen8-step4-pos-app-85.azurewebsites.net",  # フロントエンドのURL
        "http://localhost:3000"  # ローカル開発用
    ],
    allow_credentials=True,
    allow_methods=["*"],  # すべてのHTTPメソッドを許可
    allow_headers=["*"]   # すべてのヘッダーを許可
)

# ... 既存のルート定義 ... 