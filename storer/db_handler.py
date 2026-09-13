import sqlite3
import logging
import traceback
from storer.db_helpers import parse_db_records
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
                INSERT INTO comments (id, author, author_id, author_type, created_time, comment_text, analyzed)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (
                comment.get('id'),
                comment.get('author'),
                comment.get('author_id'),
                comment.get('author_type'),
                comment.get('created_time'),
                comment.get('comment_text'),
                False
            ))
            self.conn.commit()
            logging.info(f'Successfully inserted comment id {self.cursor.lastrowid}')
        except sqlite3.IntegrityError:
            logging.info(f'Comment entry already exists, skipping...')

        except Exception as e:
            logging.error(f'Failed inserting comment id {comment.get('id')} into db')
            traceback.print_exc()

    def mark_comment_analyzed(self, comment_id: str):

        try:
            logging.info(f"Marking comment id {comment_id} as successfully analyzed")
            self.cursor.execute("""
                UPDATE comments SET analyzed = ? WHERE id = ?
            """, (
                True,
                comment_id
            ))
            self.conn.commit()
            logging.info(f"Updated comment id {self.cursor.lastrowid} analyzed status to True")

        except Exception as e:
            logging.error(f"Error updating comment id {comment_id} analyzed status")
            traceback.print_exc()


    def store_roberta_scores(self, comment_id: str, scores: dict):
        
        try:
            logging.info(f"Inserting scores for comment id - {comment_id} in DB")
            self.cursor.execute("""
                INSERT INTO roberta_scores (id, comment_id, score_negative, score_neutral, score__positive)
                VALUES (?, ?, ?, ?, ?)
            """, (
                scores.get("id"),
                comment_id,
                scores.get('negative'),
                scores.get("neutral"),
                scores.get("positive")
            ))
            self.conn.commit()
            logging.info(f'Successfully inserted score id {self.cursor.lastrowid}')

        except sqlite3.IntegrityError:
            logging.info(f"Score entry already exists, skipping...")

        except Exception as e:
            logging.error(f'Failed inserting score id {scores.get("id")} into db')
            traceback.print_exc()

    def un_analyzed_comments(self):

        columns = {
            "comment_id": 0,
            "comment_text": 1
        }

        try:
            logging.info("Getting all un-analyzed comment data from DB")
            self.cursor.execute("""
                SELECT id, comment_text FROM comments WHERE analyzed = ?
            """, (
                False,
            ))
            comments_data = self.cursor.fetchall()

            return parse_db_records(comments_data, columns)
            
        except Exception as e:
            logging.error(f"Error retrieving un-analyzed comments from db {e}")
            traceback.print_exc()



    def terminate_connection(self):
        logging.info('Terminating db connection...')
        try:
            self.conn.close()
            logging.info('Terminated db connection successfully')
        except Exception as e:
            logging.error(f'Error terminating connection - {e}')