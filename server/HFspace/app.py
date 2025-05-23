import os
import json
import gradio as gr

from autoparse.parser import Parser
from autoparse.tools.converter.json_to_text import convert_json_to_text

API_KEY   = os.getenv("MISTRAL_API_KEY", None)
LLM_MODEL = os.getenv("LLM_MODEL", None)
CACHE_DIR = os.getenv("CACHE_DIR", None)
parser = Parser(cache_dir=CACHE_DIR, api_key=API_KEY, model=LLM_MODEL)


def run_parse(url: str, query: str, mode: str, meta: str):
    """
    url: страница для парсинга
    query: что именно нужно извлечь
    mode: 'structuring' или 'codegen'
    meta: CSV список полей для structuring
    """
    if mode == "structuring":
        meta_list = [m.strip() for m in meta.split(",") if m.strip()]
    else:
        meta_list = []

    result = parser.parse_url(
        url=url,
        meta=meta_list,
        user_query=query,
        mode=mode,
        dynamic=False
    )

    text = convert_json_to_text(result)
    # для codegen выводим только JSON
    raw_json = json.dumps(result, ensure_ascii=False, indent=2)

    return text, raw_json


with gr.Blocks(title="AutoParse HF Space", analytics_enabled=False) as demo:
    gr.Markdown(
        "## Автоматический парсер сайтов на основе LLM\n"
        "Введите URL, запрос (Query), выберите режим и нажмите **Parse**."
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

    def toggle_meta(mode):
        return gr.update(visible=(mode == "structuring"))

    mode_radio.change(
        fn=toggle_meta,
        inputs=[mode_radio],
        outputs=[meta_input]
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

    parse_btn.click(
        fn=run_parse,
        inputs=[url_input, query_input, mode_radio, meta_input],
        outputs=[structured_out, json_out]
    )

    demo.queue()

if __name__ == "__main__":
    demo.launch()
