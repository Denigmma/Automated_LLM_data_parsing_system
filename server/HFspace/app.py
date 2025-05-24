import os
import json
import gradio as gr

from autoparse.parser import Parser
from autoparse.tools.converter.json_to_text import convert_json_to_text

API_KEY   = os.getenv("MISTRAL_API_KEY", None)
LLM_MODEL = os.getenv("LLM_MODEL", None)
CACHE_DIR = os.getenv("CACHE_DIR", None)
parser = Parser(cache_dir=CACHE_DIR, api_key=API_KEY, model=LLM_MODEL)


def run_parse(
    url: str,
    query: str,
    mode: str,
    meta: str,
    regenerate: bool
):
    """
    url: страница для парсинга
    query: что именно нужно извлечь
    mode: 'structuring' или 'codegen'
    meta: CSV список полей для structuring
    regenerate: флаг принудительной перегенерации парсера
    """
    # собираем meta_list только для structuring
    if mode == "structuring":
        meta_list = [m.strip() for m in meta.split(",") if m.strip()]
    else:
        meta_list = []

    # передаём флаг regenerate в ядро парсинга
    result = parser.parse_url(
        url=url,
        meta=meta_list,
        user_query=query,
        mode=mode,
        dynamic=False,
        regenerate=regenerate
    )

    # текстовое представление
    text = convert_json_to_text(result)
    # JSON-вывод
    raw_json = json.dumps(result, ensure_ascii=False, indent=2)

    return text, raw_json


with gr.Blocks(title="AutoParse HF Space", analytics_enabled=False) as demo:
    gr.Markdown(
        """
        # Автоматический парсер сайтов на основе LLM

        ## Возможности:

        Предоставлены два способа парсинга:
    
        1. **Structuring Text**  
           Семантически извлекает и структурирует информацию по запросу, а так же выделяет мета-данные
    
        2. **Generate Parser**  
        Генерирует Python-скрипт-парсер, затем этот код кэшируется для быстрого повторного использования. При следующих запросах с теми же URL и похожими Query вы получите уже закешированную версию скрипта, а включив флаг **Regenerate parser code**, принудительно создадите новый код.

    
        ### Как пользоваться:
                **Как пользоваться:**  
        1. Введите **URL** страницы.  
        2. Введите **Query** — что нужно извлечь.  
        3. Выберите режим:
           - **Structuring** — структурирует текст, извлекая указанные через запятую поля.  
           - **Codegen** — генерирует и выполняет код-парсер.
        4. (Только в Codegen) Опционально включите **Regenerate parser code** для принудительной перегенерации, даже если парсер уже есть в кеше.  
        5. Нажмите **Parse** и посмотрите результат в двух панелях:
           - **Structured Text** — ответ в формате текста.  
           - **Raw JSON** — ответ в формате JSON.
        """
    )

    with gr.Row():
        url_input = gr.Textbox(
            label="URL для парсинга",
            placeholder="https://example.com",
            lines=1
        )
        query_input = gr.Textbox(
            label="Query",
            placeholder="Что именно нужно извлечь?",
            lines=1
        )
        mode_radio = gr.Radio(
            choices=["structuring", "codegen"],
            value="structuring",
            label="Режим парсинга"
        )

    meta_input = gr.Textbox(
        label="Metadata fields (comma-separated)",
        placeholder="City, Current temperature",
        visible=True
    )

    regenerate_checkbox = gr.Checkbox(
        label="Regenerate parser code",
        value=False,
        visible=False
    )

    def toggle_visibility(mode):
        return (
            gr.update(visible=(mode == "structuring")),
            gr.update(visible=(mode == "codegen"))
        )

    mode_radio.change(
        fn=toggle_visibility,
        inputs=[mode_radio],
        outputs=[meta_input, regenerate_checkbox]
    )

    parse_btn = gr.Button("Parse")

    with gr.Row():
        structured_out = gr.Textbox(
            label="Structured Text",
            lines=10,
            interactive=False
        )
        json_out = gr.Code(
            label="Raw JSON",
            language="json"
        )

    # Добавляем regenerate_checkbox в список inputs
    parse_btn.click(
        fn=run_parse,
        inputs=[url_input, query_input, mode_radio, meta_input, regenerate_checkbox],
        outputs=[structured_out, json_out]
    )

    demo.queue()

if __name__ == "__main__":
    demo.launch()
