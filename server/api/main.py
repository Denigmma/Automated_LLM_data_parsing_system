# server/api/main.py

import os
from typing import Optional

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

from autoparse.parser import Parser

app = FastAPI(
    title="AutoParse API",
    description="LLM-driven HTML parser — отдаёт JSON с чистым текстом и метаданными",
    version="1.0.0",
)

class ParseRequest(BaseModel):
    url: str = Field(..., example="https://example.com")
    mode: Optional[str] = Field("auto", description="auto | structuring | codegen")
    dynamic: Optional[bool] = Field(False, description="JS-рендеринг через Selenium")
    llm_api_key: Optional[str] = Field(
        None,
        description="Ваш API-ключ для LLM (если не указан, будет использовано MISTRAL_API_KEY из окружения)"
    )
    llm_model: Optional[str] = Field(
        None,
        description="Модель LLM (если не указана, будет использовано LLM_MODEL из окружения)"
    )

@app.post("/parse", summary="Парсит страницу и возвращает JSON")
async def parse(req: ParseRequest):
    # 1) Получаем ключ
    api_key = req.llm_api_key or os.getenv("MISTRAL_API_KEY")
    if not api_key:
        raise HTTPException(
            status_code=400,
            detail="Не передан API-ключ LLM (параметр llm_api_key или переменная MISTRAL_API_KEY)"
        )

    # 2) Инициализируем парсер
    try:
        parser = Parser(
            api_key=api_key,
            model=req.llm_model
        )
        result = parser.parse_url(
            url=req.url,
            meta={},           # meta для structuring можно расширить по желанию
            mode=req.mode,
            dynamic=req.dynamic
        )
        return result

    except Exception as e:
        # Пробрасываем ошибку как HTTP 500
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/ping", summary="Health check")
async def ping():
    return {"status": "ok"}
