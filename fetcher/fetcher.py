from playwright.sync_api import sync_playwright
from extractors import fb_extractor
from parsers.general_parser import background_parser
from global_consts.api import LISTENING_PORT
from global_consts.base_consts import RAW_SAVE_DIR
from storer.db_handler import DBHandler
from storer.storer import Storer
import logging
import json
import os
import time
import subprocess
import threading
import traceback

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)


class Fetcher:

    db: DBHandler

    def __init__(self):
        
        logging.info('Starting chromium instance in port 9222')

        subprocess.Popen([
            "brave-browser",
            "--remote-debugging-port=9222",
            "--user-data-dir=/tmp/brave_dev_session"
        ])
        self.db = DBHandler()

        time.sleep(2)

        os.makedirs(RAW_SAVE_DIR, exist_ok=True)

    def start_watcher(self, stop_event):

        with sync_playwright() as p:
            # Connect to active Chromium session
            browser = p.chromium.connect_over_cdp(LISTENING_PORT)
            context = browser.contexts[0]

            context.on('response', self.handle_response)
            
            logging.info(f"Listening to port {LISTENING_PORT} \nScroll in browser's feed to grab responses.")
            logging.info("Press CRTL + C to terminate")

            page = context.pages[0]
            
            # INFINITE LOOP (No 60 second limit!)

            while not stop_event.is_set():
                page.wait_for_timeout(1000)

            logging.info("\nTerminated browser connection.")
            logging.info('Waiting for thread workers to finish...')
            browser.close()
            time.sleep(2)
            storer = Storer(self.db)
            storer.get_parsed_files()
            storer.store_comment_data()
            storer.cleanup_data()

    def handle_response(self, response):

        data = fb_extractor.fb_req_detector(response)

        if isinstance(data, dict) and data.get('data'):
            raw_data = data.get('data')
            data_flag = data.get('flag')
            filename = f"{RAW_SAVE_DIR}/facebook-feed_{time.time()}.json"
            try:

                with open(filename, "w") as f:
                    json.dump(raw_data, f)
                    print(f"Saved network packet: {filename}")

                thread = threading.Thread(target=background_parser, args=(filename, data_flag))
                thread.start()
                
            except Exception as e:
                print(f'Failed saving the response packet {e}')
                traceback.print_exc()
                pass