from storer.db_handler import DBHandler
from storer import storer
from parsers import fb_comment_parser
from global_consts.base_consts import PARSED_SAVE_DIR
import logging
import traceback
import time
import json

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

def background_parser(file_path: str, flag: str):
    try:
        with open(file_path, 'r') as parse_file:
            body = json.load(parse_file)
            nodes = fb_comment_parser.get_nodes_from_response(body, flag)

            parsed_nodes = fb_comment_parser.parse_nodes_from_response(nodes)

            parsed_file_path = f'{PARSED_SAVE_DIR}/facebook-parsed-comments_{time.time()}.json'

            with open(parsed_file_path, 'w') as parsed_save:
                json.dump(parsed_nodes, parsed_save)

    except Exception as e:
        logging.error(f'Error parsing file: {file_path} due to: {e}')
        traceback.print_exc()
        pass

