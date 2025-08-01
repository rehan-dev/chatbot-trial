from fastapi import FastAPI
from app import models, database
from app.auth import router as auth_router
from app.chat import router as chat_router

models.Base.metadata.create_all(bind=database.engine)

app = FastAPI(title="Chatbot APIs")

app.include_router(auth_router)
app.include_router(chat_router)
