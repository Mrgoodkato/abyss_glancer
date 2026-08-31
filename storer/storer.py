from storer.db_handler import DBHandler
import json
import hashlib
import logging
import traceback


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

def store_single_parsed_data(file_path: str, db_handler: DBHandler):
    try:
        with open(file_path, 'r') as tmp_file:
            logging.info(f'Storing comments for parsed file - {file_path}')
            body = json.load(tmp_file)

            for comment_data in body:
                comment_row = _prepare_comment_data(comment_data)
                db_handler.store_comment(comment_row)


    except Exception as e:
        logging.error(f'Error storing comment info from file - {file_path}')
        traceback.print_exc()
        pass


def _prepare_comment_data(comment_item: dict):

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