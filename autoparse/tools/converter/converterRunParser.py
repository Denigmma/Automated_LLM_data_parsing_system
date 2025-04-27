import subprocess
import sys
import tempfile
import os
from typing import Dict

def run_and_convert_parser(parser_code: str, html: str) -> Dict[str, str]:
    """
    Execute the generated parser code on the given HTML and
    wrap its stdout into a {"cleaned_text": "..."} dict.

    Args:
      parser_code: Python code (as string) from LLM.
      html:        The raw HTML to feed into the parser via stdin.

    Returns:
      A dict with one key "cleaned_text": the full stdout of the parser.

    Raises:
      RuntimeError if the parser subprocess exits with non-zero.
    """
    # Создаём временную папку, чтобы не засорять кеш
    with tempfile.TemporaryDirectory() as tmpdir:
        parser_path = os.path.join(tmpdir, "parser.py")
        # Записываем код-парсер
        with open(parser_path, "w", encoding="utf-8") as f:
            f.write(parser_code)

        # Запускаем его, передавая HTML на stdin
        env = os.environ.copy()
        env["PYTHONIOENCODING"] = "utf-8"
        proc = subprocess.run(
            [sys.executable, parser_path],
            input=html,
            capture_output=True,
            text=True,
            encoding = "utf-8",
            errors = "strict",
            env=env
        )

        if proc.returncode != 0:
            # Если парсер упал, отдаём stderr в ошибке
            raise RuntimeError(
                f"Parser execution failed (code {proc.returncode}):\n{proc.stderr}"
            )

        output = proc.stdout

    # Возвращаем ровно тот JSON, который ждёт UI
    return {"cleaned_text": output}