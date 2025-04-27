CREATE TABLE IF NOT EXISTS code_cache (
  url         TEXT PRIMARY KEY,
  file_path   TEXT NOT NULL,
  created_at  TEXT NOT NULL,
  updated_at  TEXT NOT NULL
);