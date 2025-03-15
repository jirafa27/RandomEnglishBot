from fastapi import FastAPI
from api.routes import user_routes, chat_routes

app = FastAPI(title="EnglishClub API")

app.include_router(user_routes, prefix="/users", tags=["Users"])
app.include_router(chat_routes, prefix="/chats", tags=["Chats"])


@app.get("/")
def home():
    return {"message": "Welcome to EnglishClub API"}
