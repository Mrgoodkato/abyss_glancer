import requests
import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

HEADERS = {
    "ngrok-skip-browser-warning": "true", # Magic mark!
    "Content-Type": "application/json"
}

def _send_payload(payload: dict, url: str):
    try:
        response = requests.post(url, headers=HEADERS, json=payload)

        if response.status_code == 200:
            data = response.json()
            logging.info(f"Successful API request to google Colab - to {url}")
            return data
        else:
            logging.error(f"Error in API call - {response.status_code} - to {url}")
            logging.error(response.text)
            return None

    except Exception as e:
        logging.error(f"Connection to API in Colab failed - {url}\nError: {e}")
        return None

def analyze_comment(url: str, comment_text: str):
    payload = {
        "text": comment_text
    }

    return _send_payload(payload, url)

def analyze_text_logit_per_user(url: str, author_comment_payload: dict):
    
    payload = {
        "user_id": author_comment_payload["author_id"],
        "user_text": author_comment_payload["comment_payload"]
    }

    return _send_payload(payload, url)