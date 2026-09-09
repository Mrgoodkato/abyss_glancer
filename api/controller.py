import requests
import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

def analyze_comment(url: str, comment_text: str):
    payload = {
        "text": comment_text
    }

    headers = {
        "ngrok-skip-browser-warning": "true", # Magic mark!
        "Content-Type": "application/json"   
    }

    try:
        response = requests.post(url, headers=headers, json=payload)

        if response.status_code == 200:
            data = response.json()
            logging.info("Successful API request to google Colab")
            return data
        else:
            logging.error(f"Error in API call - {response.status_code}")
            logging.error(response.text)
            return None

    except Exception as e:
        logging.error(f"Connection to API in Colab failed {e}")

