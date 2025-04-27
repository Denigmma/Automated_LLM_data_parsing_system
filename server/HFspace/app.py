import os
import json
import gradio as gr

from autoparse.parser import Parser

# Считываем ключи из переменных окружения (если нужны для LLMClient)
API_KEY = os.getenv("MISTRAL_API_KEY", None)
LLM_MODEL = os.getenv("LLM_MODEL", None)
CACHE_DIR = os.getenv("CACHE_DIR", None)

# Инстанцируем наш парсер
parser = Parser(cache_dir=CACHE_DIR, api_key=API_KEY, model=LLM_MODEL)

def run_parse(
    url: str,
    mode: str,
    dynamic: bool
) -> str:
    """
    Вызывается при нажатии кнопки «Parse».
    Возвращает результат в виде отформатированного JSON.
    """
    try:
        # Парсим страницу
        result = parser.parse_url(url, meta={}, mode=mode, dynamic=dynamic)
        # Приводим к строке
        return json.dumps(result, ensure_ascii=False, indent=2)
    except Exception as e:
        return json.dumps({"error": str(e)}, ensure_ascii=False, indent=2)


# --- Графический интерфейс ---
with gr.Blocks(
    title="AutoParse HF Space",
    analytics_enabled=False
) as demo:

    gr.Markdown("## Автоматический парсер сайтов на основе LLM\n"
                "Введите URL, выберите режим и нажмите **Parse**.")

    with gr.Row():
        url_input = gr.Textbox(label="URL для парсинга", placeholder="https://example.com")
        mode_radio = gr.Radio(
            choices=["auto", "structuring", "codegen"],
            value="auto",
            label="Режим парсинга"
        )
        dynamic_chk = gr.Checkbox(label="JS-рендеринг (Selenium)", value=False)

    parse_btn = gr.Button("Parse")
    output = gr.Code(label="Результат (JSON)", language="json")

    parse_btn.click(
        fn=run_parse,
        inputs=[url_input, mode_radio, dynamic_chk],
        outputs=[output],
    )

if __name__ == "__main__":
    demo.launch(
        server_name="0.0.0.0",
        server_port=int(os.getenv("PORT", 7860))
    )
