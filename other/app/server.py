from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates
import uvicorn
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
templates = Jinja2Templates(directory=os.path.join(BASE_DIR, "templates"))

from other.app.interface import process_user_message

app = FastAPI()

@app.get("/", response_class=HTMLResponse)
async def get_chat(request: Request):
    """
    Эндпоинт для отдачи HTML-страницы с интерфейсом чата.
    """
    return templates.TemplateResponse("chat.html", {"request": request})

@app.post("/chat", response_class=JSONResponse)
async def chat_endpoint(message: str = Form(...)):
    """
    Эндпоинт для приёма сообщения от пользователя.
    Обрабатывает сообщение с помощью process_user_message и возвращает ответ.
    """
    response_text = process_user_message(message)
    return {"response": response_text}

if __name__ == "__main__":
    uvicorn.run("app.server:app", host="0.0.0.0", port=8000, reload=True)
