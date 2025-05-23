UPDATE code_cache
   SET file_path   = :file_path,
       updated_at  = :updated_at
 WHERE url          = :url
   AND user_query   = :user_query;

INSERT OR IGNORE INTO code_cache (
  url,
  user_query,
  file_path,
  created_at,
  updated_at
) VALUES (
  :url,
  :user_query,
  :file_path,
  :created_at,
  :updated_at
);