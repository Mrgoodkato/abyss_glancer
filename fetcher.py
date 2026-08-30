from playwright.sync_api import sync_playwright
from parsers import fb_comment_parser
from extractors import fb_extractor
import logging
import json
import os
import time
import subprocess
import threading
import traceback


RAW_SAVE_DIR = "./fetched_data"
PARSED_SAVE_DIR = './parsed_data'

LISTENING_PORT = 'http://localhost:9222'

FB_HEADER_INFO = {
    "header": "x-fb-friendly-name",
    "header_val": "CometSinglePostDialogContentQuery"
}

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

logging.info('Starting chromium instance in port 9222')

subprocess.Popen([
    "brave-browser",
    "--remote-debugging-port=9222",
    "--user-data-dir=/tmp/brave_dev_session"
])

time.sleep(2)

os.makedirs(RAW_SAVE_DIR, exist_ok=True)

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


def handle_response(response):

    data = fb_extractor.fb_req_detector(response)

    if isinstance(data, dict) and data.get('data'):
        raw_data = data.get('data')
        data_flag = data.get('flag')
        filename = f"{RAW_SAVE_DIR}/facebook-feed_{time.time()}.json"
        try:

            with open(filename, "w") as f:
                json.dump(raw_data, f)
                print(f"Saved network packet: {filename}")

            thread = threading.Thread(target=background_parser, args=(filename,data_flag))
            thread.start()
            
        except Exception as e:
            print(f'Failed saving the response packet {e}')
            traceback.print_exc()
            pass
        



                
with sync_playwright() as p:
    # Connect to active Chrome session
    browser = p.chromium.connect_over_cdp(LISTENING_PORT)
    context = browser.contexts[0]

    context.on('response', handle_response)
    
    logging.info(f"Listening to port {LISTENING_PORT} - Scroll in browser's feed to grab responses.")
    logging.info("Press CRTL + C to terminate")

    page = context.pages[0]
    
    # INFINITE LOOP (No 60 second limit!)
    try:
        while True:
            page.wait_for_timeout(1000)
    except KeyboardInterrupt:
        logging.info("\nTerminated program.")
        traceback.print_exc()