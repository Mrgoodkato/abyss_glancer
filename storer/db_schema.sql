CREATE TABLE IF NOT EXISTS comments (
    id TEXT UNIQUE NOT NULL PRIMARY KEY,
    author TEXT NOT NULL,
    author_id TEXT NOT NULL,
    author_type TEXT,
    created_time NUMBER NOT NULL,
    comment_text TEXT,
    analyzed BOOLEAN NOT NULL
);

CREATE TABLE IF NOT EXISTS roberta_scores (
    id TEXT UNIQUE NOT NULL PRIMARY KEY,
    comment_id TEXT UNIQUE NOT NULL,
    score_negative FLOAT NOT NULL,
    score_neutral FLOAT NOT NULL,
    score_positive FLOAT NOT NULL,
    FOREIGN KEY (comment_id) REFERENCES comments(id)
);