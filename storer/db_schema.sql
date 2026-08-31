CREATE TABLE IF NOT EXISTS comments (
    id TEXT UNIQUE NOT NULL PRIMARY KEY,
    author TEXT NOT NULL,
    author_id TEXT NOT NULL,
    author_type TEXT,
    created_time NUMBER NOT NULL,
    comment_text TEXT
)