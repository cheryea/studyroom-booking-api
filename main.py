from fastapi import FastAPI

from database import engine
from app import models

from app.routers.auth_router import router as auth_router
from app.routers.user_router import router as user_router

# 정의된 모델들을 기반으로 DB에 테이블을 생성한다.
models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(auth_router)
app.include_router(user_router)

@app.get("/")
def read_root():
    return {"Hello": "World"}

