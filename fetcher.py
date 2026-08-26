from playwright.sync_api import sync_playwright
from parsers import fb_comment_parser
import json
import os
import time
import subprocess
import threading
import traceback

print('Starting chromium instance in port 9222')
subprocess.Popen([
    "brave-browser",
    "--remote-debugging-port=9222",
    "--user-data-dir=/tmp/brave_dev_session"
])

time.sleep(2)

RAW_SAVE_DIR = "./fetched_data"
PARSED_SAVE_DIR = './parsed_data'

FB_HEADER_INFO = {
    "header": "x-fb-friendly-name",
    "header_val": "CometSinglePostDialogContentQuery"
}
os.makedirs(RAW_SAVE_DIR, exist_ok=True)

def background_parser(file_path: str):
    try:
        with open(file_path, 'r') as parse_file:
            body = json.load(parse_file)
            print(type(body))
            nodes = fb_comment_parser.get_nodes_from_response(body)

            parsed_nodes = fb_comment_parser.parse_nodes_from_response(nodes)

            parsed_file_path = f'{PARSED_SAVE_DIR}/facebook-parsed-comments_{time.time()}.json'

            with open(parsed_file_path, 'w') as parsed_save:
                json.dump(parsed_nodes, parsed_save)

    except Exception as e:
        print(f'Error parsing file: {file_path} due to: {e}')
        traceback.print_exc()
        pass


def handle_response(response):
    # Filter for Facebook GraphQL network payloads
    req = response.request
    req_headers = req.headers
    
    
    if "api/graphql/" in response.url and response.status == 200:
        
        if FB_HEADER_INFO.get('header') in req_headers:
            
            if req_headers.get(FB_HEADER_INFO['header']) == FB_HEADER_INFO['header_val']:
                print(f'Found response with header {FB_HEADER_INFO['header']} - and value: {FB_HEADER_INFO["header_val"]}')
                print(response.url[:80])

                data = []
                
                stacked_payload = response.text()
                lines = stacked_payload.splitlines()

                for line in lines:
                    if not line.strip():
                        continue

                    try:
                        body = json.loads(line)
                        print('Created body')
                        data.append(body)        

                    except Exception as e:
                        print(f'Failed saving the response due to: {e}')
                        traceback.print_exc()
                        pass
                        
                filename = f"{RAW_SAVE_DIR}/facebook-feed_{time.time()}.json"
                try:

                    with open(filename, "w") as f:
                        json.dump(data, f)
                        print(f"Saved network packet: {filename}")

                    thread = threading.Thread(target=background_parser, args=(filename,))
                    thread.start()
                    
                except Exception as e:
                    print(f'Failed saving the response packet {e}')
                    traceback.print_exc()
                    pass
                



                
with sync_playwright() as p:
    # Connect to active Chrome session
    browser = p.chromium.connect_over_cdp("http://localhost:9222")
    context = browser.contexts[0]

    context.on('response', handle_response)
    
    print("Listening forever! Scroll feed in browser.")
    print("Press CRTL + C to terminate")

    page = context.pages[0]

    page.reload()
    
    # INFINITE LOOP (No 60 second limit!)
    try:
        while True:
            page.wait_for_timeout(1000)
    except KeyboardInterrupt:
        print("\nTerminated program.")
        traceback.print_exc()