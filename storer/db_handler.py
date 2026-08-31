import sqlite3
import logging
import traceback
from pathlib import Path

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

class DBHandler:
    BASE_DIR = Path(__file__).resolve().parent
    TMP_STORAGE_DB = BASE_DIR / 'tmp_storage' / 'app.db'
    schema_path = BASE_DIR / 'db_schema.sql'
    conn: sqlite3.Connection
    cursor: sqlite3.Cursor

    def __init__(self):
        try:
            self.TMP_STORAGE_DB.parent.mkdir(parents=True, exist_ok=True)

            logging.info(f'Connecting to db in {self.TMP_STORAGE_DB}')
            self.conn = sqlite3.connect(self.TMP_STORAGE_DB)
            self.cursor = self.conn.cursor()

            logging.info('Checking PRGAMA version...')
            self.cursor.execute("PRAGMA user_version;")
            current_version = self.cursor.fetchone()[0]

            if current_version < 1:
                logging.info(f'Setting up db schema for comments from schema in {self.schema_path}')
                with open(self.schema_path, 'r') as schema_file:
                    schema_sql = schema_file.read()

                self.cursor.executescript(schema_sql)

        except Exception as e:
            logging.error(f'Failed to connect to DB in {self.TMP_STORAGE_DB}')
            traceback.print_exc()


    def store_comment(self, comment: dict):

        try:
            logging.info(f'Inserting comment with id {comment.get('id')} into db')
            self.cursor.execute("""
                INSERT INTO comments (id, author, author_id, author_type, created_time, comment_text)
                VALUES (?, ?, ?, ?, ?)
            """, (
                comment.get('id'),
                comment.get('author'),
                comment.get('author_id'),
                comment.get('author_type'),
                comment.get('created_time'),
                comment.get('comment_text')
            ))
            self.conn.commit()
            logging.info(f'Successfully inserted comment id {self.cursor.lastrowid}')

        except Exception as e:
            logging.error(f'Failed inserting comment id {comment.get('id')} into db')
            traceback.print_exc()
        