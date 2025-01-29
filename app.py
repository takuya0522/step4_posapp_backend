from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI()

# CORS設定を更新
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Message(BaseModel):
    message: str

@app.get("/")
async def hello():
    return {"message": "Flask start!"}

@app.get("/api/hello")
async def hello_world():
    return {"message": "Hello World by FastAPI"}

@app.get("/api/multiply/{id}")
async def multiply(id: int):
    print("multiply")
    # idの2倍の数を計算
    doubled_value = id * 2
    return {"doubled_value": doubled_value}

@app.post("/api/echo")
async def echo(data: Message):
    print("echo")
    # 'message' プロパティが含まれていることを確認
    return {"message": f"echo: {data.message}"}

