import os
import sqlite3
import hashlib
from datetime import datetime
from typing import Optional

# путь к sql-файлам
SQL_DIR = os.path.join(os.path.dirname(__file__), "sql")
CREATE_TABLE_SQL = os.path.join(SQL_DIR, "create_code_cache_table.sql")
UPSERT_SQL = os.path.join(SQL_DIR, "upsert_code_cache.sql")


class ParserCodeCache:
    """
    Cache for storing LLM-generated parser code, with SQL separated into .sql files.
    """

    def __init__(self, base_dir: str):
        self.code_dir = os.path.join(base_dir, "parsers")
        os.makedirs(self.code_dir, exist_ok=True)
        self.db_path = os.path.join(base_dir, "cache.db")
        self._init_db()

    def _init_db(self):
        """Initialize SQLite DB schema from .sql file."""
        con = sqlite3.connect(self.db_path)
        with open(CREATE_TABLE_SQL, "r", encoding="utf-8") as f:
            ddl = f.read()
        con.executescript(ddl)
        con.commit()
        con.close()

    def _url_hash(self, url: str) -> str:
        return hashlib.sha256(url.encode("utf-8")).hexdigest()[:16]

    def get(self, url: str) -> Optional[str]:
        """Return cached code or None."""
        con = sqlite3.connect(self.db_path)
        cur = con.execute(
            "SELECT file_path FROM code_cache WHERE url = ?",
            (url,)
        )
        row = cur.fetchone()
        con.close()
        if not row:
            return None
        path = os.path.join(self.code_dir, row[0])
        if not os.path.isfile(path):
            return None
        with open(path, "r", encoding="utf-8") as f:
            return f.read()

    def store(self, url: str, code: str) -> None:
        """
        Store or update parser code:
         - Write .py file
         - Execute upsert SQL from file
        """
        filename = f"{self._url_hash(url)}.py"
        file_path = os.path.join(self.code_dir, filename)

        # 1) write code to file
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(code)

        # 2) upsert metadata
        now = datetime.utcnow().isoformat()
        params = {
            "url": url,
            "file_path": filename,
            "created_at": now,
            "updated_at": now
        }

        con = sqlite3.connect(self.db_path)
        cur = con.cursor()
        # Читаем SQL-скрипт, делим по ';' и выполняем каждый запрос с параметрами
        with open(UPSERT_SQL, "r", encoding="utf-8") as f:
            for stmt in f.read().split(";"):
                stmt = stmt.strip()
                if not stmt:
                    continue
                cur.execute(stmt, params)
        con.commit()
        con.close()
