from dotenv import load_dotenv
load_dotenv()

from typing import List, Optional

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from autoparse.tools.converter.json_to_text import convert_json_to_text

from agent.agent import run_agent

import logging
import logging.config
from pathlib import Path
import yaml

# находим корень проекта (две папки вверх от текущего файла)
BASE_DIR = Path(__file__).resolve().parents[2]
LOG_CFG = BASE_DIR / "config" / "logging.yaml"

if LOG_CFG.exists():
    cfg = yaml.safe_load(LOG_CFG.read_text(encoding="utf-8"))
    logging.config.dictConfig(cfg)
else:
    # fallback — простой вывод в консоль
    logging.basicConfig(level=logging.INFO)
    logging.getLogger(__name__).warning(f"Не найден {LOG_CFG}, использую базовое логирование")

app = FastAPI()
app.mount("/static", StaticFiles(directory="server/web/static"), name="static")
templates = Jinja2Templates(directory="server/web/templates")


class ParseRequest(BaseModel):
    url:  str
    mode: str
    meta: Optional[str] = None


@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.post("/parse/")
async def parse(req: ParseRequest):
    # guaranteed: req.url and req.mode exist
    if req.mode == "structuring":
        raw = req.meta or ""
        meta_list: List[str] = [m.strip() for m in raw.split(",") if m.strip()]
    else:
        meta_list = []

    try:
        result = run_agent(
            url=req.url,
            meta=meta_list,
            mode=req.mode,
            dynamic=None
        )
        result_text = convert_json_to_text(result)
        return JSONResponse(content={"json": result,"text": result_text})
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})
