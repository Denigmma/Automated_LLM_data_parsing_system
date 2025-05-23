from dotenv import load_dotenv

load_dotenv()

import os
import sqlite3
import uuid
from datetime import datetime
from typing import Optional
from chromadb import Client
from chromadb.utils import embedding_functions

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

        self.embed_model = os.getenv(
            "EMBEDDING_MODEL_NAME",
            "paraphrase-multilingual-MiniLM-L12-v2"
        )
        self.threshold = float(os.getenv("CACHE_THRESHOLD", "0.85"))

        self.chroma_client = Client()

        hf_token = os.getenv("HUGGINGFACE_HUB_TOKEN")
        self.collection = self.chroma_client.get_or_create_collection(
            name="code_cache",
            embedding_function=embedding_functions.SentenceTransformerEmbeddingFunction(
                model_name=self.embed_model,
                use_auth_token=hf_token,
                trust_remote_code=True
            ),
            metadata={"hnsw:space": "cosine"}
        )
        self._load_existing_embeddings()

    def _load_existing_embeddings(self) -> None:
        """
        Загрузка user_query-эмбеддингов в ChromaDB из SQLite.
        """
        con = sqlite3.connect(self.db_path)
        cur = con.cursor()
        cur.execute("SELECT url, user_query, file_path FROM code_cache")
        for url, user_query, file_path in cur.fetchall():
            # идентификатор записи в коллекции
            doc_id = f"{url}:{user_query}"
            self.collection.add(
                ids=[doc_id],
                documents=[user_query],
                metadatas=[{"url": url, "file_path": file_path}]
            )
        con.close()

    def find_similar(self, url: str, user_query: str) -> Optional[dict]:
        """
        Семантический поиск в ChromaDB по url + user_query.
        Возвращает {'file_path': str, 'similarity': float} при совпадении,
        иначе None.
        """
        results = self.collection.query(
            query_texts=[user_query],
            n_results=1,
            where={"url": {"$eq": url}}
        )

        # Извлекаем три ключевых поля из ответа
        distances = results.get("distances", [])
        ids = results.get("ids", [])
        metas = results.get("metadatas", [])

        if (
                distances
                and isinstance(distances[0], list)
                and len(distances[0]) > 0
                and ids
                and isinstance(ids[0], list)
                and len(ids[0]) > 0
                and metas
                and isinstance(metas[0], list)
                and len(metas[0]) > 0
        ):
            dist = distances[0][0]
            # Проверяем порог близости
            if 1 - dist >= self.threshold:
                file_path = metas[0][0].get("file_path")
                return {
                    "file_path": file_path,
                    "similarity": 1 - dist
                }

        return None

    def _init_db(self):
        """Initialize SQLite DB schema from .sql file."""
        con = sqlite3.connect(self.db_path)
        with open(CREATE_TABLE_SQL, "r", encoding="utf-8") as f:
            ddl = f.read()
        con.executescript(ddl)
        con.commit()
        con.close()

    def _generate_filename(self) -> str:
        """Generate a unique filename for a new parser."""
        return f"{uuid.uuid4().hex}.py"

    def get(self, url: str, user_query: str) -> Optional[str]:
        """Return cached code for this (url, user_query) or None."""
        con = sqlite3.connect(self.db_path)
        cur = con.execute(
            "SELECT file_path FROM code_cache WHERE url = ? AND user_query = ?",
            (url, user_query)
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

    def store(self, url: str, user_query: str, code: str) -> None:
        """
        Store or update parser code for a given url+user_query:
         - Write .py file
         - Execute upsert SQL from file
        """
        filename = self._generate_filename()
        file_path = os.path.join(self.code_dir, filename)

        with open(file_path, "w", encoding="utf-8") as f:
            f.write(code)

        now = datetime.utcnow().isoformat()
        params = {
            "url": url,
            "user_query": user_query,
            "file_path": filename,
            "created_at": now,
            "updated_at": now
        }

        con = sqlite3.connect(self.db_path)
        cur = con.cursor()

        with open(UPSERT_SQL, "r", encoding="utf-8") as f:
            for stmt in f.read().split(";"):
                stmt = stmt.strip()
                if not stmt:
                    continue
                cur.execute(stmt, params)
        con.commit()
        con.close()

        doc_id = f"{url}:{user_query}"
        self.collection.add(
            ids=[doc_id],
            documents=[user_query],
            metadatas=[{"url": url, "file_path": filename}]
        )
