CREATE TABLE IF NOT EXISTS comments (
    id TEXT UNIQUE NOT NULL PRIMARY KEY,
    author TEXT NOT NULL,
    author_id TEXT NOT NULL,
    author_type TEXT,
    created_time NUMBER NOT NULL,
    comment_text TEXT,
    analyzed BOOLEAN NOT NULL,
    logit_parsed BOOLEAN NOT NULL
);

CREATE TABLE IF NOT EXISTS roberta_scores (
    id TEXT UNIQUE NOT NULL PRIMARY KEY,
    comment_id TEXT UNIQUE NOT NULL,
    score_negative FLOAT NOT NULL,
    score_neutral FLOAT NOT NULL,
    score_positive FLOAT NOT NULL,
    FOREIGN KEY (comment_id) REFERENCES comments(id)
);

CREATE TABLE IF NOT EXISTS logit_scores (
    id TEXT UNIQUE NOT NULL PRIMARY KEY,
    author_id TEXT UNIQUE NOT NULL,
    comment_payload TEXT UNIQUE NOT NULL,
    logit_score FLOAT NOT NULL,
    FOREIGN KEY (author_id) REFERENCES comments(author_id)
);

CREATE TABLE IF NOT EXISTS weighted_analysis (
    id TEXT UNIQUE NOT NULL PRIMARY KEY,
    confidence_score REAL
);