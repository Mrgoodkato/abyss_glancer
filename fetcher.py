from playwright.sync_api import sync_playwright
import json
import os
import time
import subprocess

print('Starting chromium instance in port 9222')
subprocess.Popen([
    "brave-browser",
    "--remote-debugging-port=9222",
    "--user-data-dir=/tmp/brave_dev_session"
])

time.sleep(2)

SAVE_DIR = "./fetched_data"
FB_HEADER_INFO = {
    "header": "x-fb-friendly-name",
    "header_val": "CometSinglePostDialogContentQuery"
}
os.makedirs(SAVE_DIR, exist_ok=True)

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
                        pass
                        
                    filename = f"{SAVE_DIR}/facebook-feed_{time.time()}.json"
                    with open(filename, "w") as f:
                        json.dump(data, f)
                    print(f"Saved network packet: {filename}")
                
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