DROP TABLE IF EXISTS headlines;


CREATE TABLE headlines (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  source_id TEXT,
  source_name TEXT,
  author TEXT,
  title TEXT,
  description TEXT,
  url TEXT,
  url_to_image TEXT,
  published_at_ts INTEGER,
  published_at TEXT,
  content TEXT
);