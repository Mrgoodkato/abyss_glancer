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
os.makedirs(SAVE_DIR, exist_ok=True)

def handle_response(response):
    # Filter for Facebook GraphQL network payloads
    print(response.url[:80])
    if "api/graphql/" in response.url and response.status == 200:

        try:
            body = response.json()
            filename = f"{SAVE_DIR}/facebook-feed_{time.time()}.json"
            with open(filename, "w") as f:
                json.dump(body, f)
            print(f"Ugh! Saved network packet: {filename}")
        except Exception:
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