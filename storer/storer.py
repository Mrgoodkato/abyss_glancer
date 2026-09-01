from storer.db_handler import DBHandler
from global_consts.base_consts import PARSED_SAVE_DIR, RAW_SAVE_DIR
from pathlib import Path
import json
import hashlib
import logging
import traceback


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

class Storer:

    PARSED_DIR = Path(PARSED_SAVE_DIR)
    RAW_DIR = Path(RAW_SAVE_DIR)

    def __init__(self, db_handler: DBHandler):
        self.db_handler: DBHandler = db_handler
        self.parsed_files: list[dict] = []

    def get_parsed_files(self):

        for parsed_file in self.PARSED_DIR.iterdir():

            if parsed_file.is_file() and parsed_file.suffix == ".json":
                with open(parsed_file, 'r', encoding="utf-8") as pf:
                    data = json.load(pf)
                    self.parsed_files.extend(data)

    def cleanup_data(self):

        logging.info(f'Removing tmp parsed data from {self.PARSED_DIR.as_posix()}')
        try:
            for file in self.PARSED_DIR.iterdir():
                if file.is_file():
                    file.unlink()

            logging.info(f'Removal operation complete for dir {self.PARSED_DIR.as_posix()}')

        except Exception as e:
            logging.error(f'Failed to remove the parsed data files from {self.PARSED_DIR.as_posix()}')
            traceback.print_exc()

        logging.info(f'Removing tmp raw data from {self.RAW_DIR.as_posix()}')
        try:
            for file in self.RAW_DIR.iterdir():
                if file.is_file():
                    file.unlink()

            logging.info(f'Removal operation complete for dir {self.RAW_DIR.as_posix()}')

        except Exception as e:
            logging.error(f'Failed to remove the raw data files from {self.RAW_DIR.as_posix()}')
            traceback.print_exc()

        self.db_handler.terminate_connection()
    

    def store_comment_data(self):
        try:
            for comment_data in self.parsed_files:
                comment_row = self._prepare_comment_data(comment_data)
                self.db_handler.store_comment(comment_row)


        except Exception as e:
            logging.error(f'Error storing comment info from dir {self.PARSED_DIR.as_posix()}')
            traceback.print_exc()
            pass


    def _prepare_comment_data(self, comment_item: dict):

        author = comment_item.get('author')
        author_id = comment_item.get('author_id_fb')
        author_type = comment_item.get('author_type_fb')
        created_time = comment_item.get('time')
        comment_text = comment_item.get('comment_text')

        combined_comment_str = f'{author}-{author_id}-{author_type}-{created_time}-{comment_text}'

        comment_bytes_val = combined_comment_str.encode('utf-8')

        comment_hash = hashlib.sha256(comment_bytes_val).hexdigest()

        return {
            "id": comment_hash,
            "author": author,
            "author_id": author_id,
            "author_type": author_type,
            "created_time": created_time,
            "comment_text": comment_text
        }