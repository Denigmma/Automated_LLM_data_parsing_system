CREATE TABLE IF NOT EXISTS code_cache (
  url         TEXT      NOT NULL,
  user_query  TEXT      NOT NULL,
  file_path   TEXT      NOT NULL,
  created_at  TEXT      NOT NULL,
  updated_at  TEXT      NOT NULL,
  PRIMARY KEY (url, user_query)
);
