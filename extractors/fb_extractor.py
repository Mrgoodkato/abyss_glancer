from global_consts.facebook import FB_URL_API, FB_HEADER_KEY, FB_HEADER_VALUES
import logging
import traceback
import json

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)



def main_comment_extract(response):
    data = []

    stacked_payload = response.text()
    lines = stacked_payload.splitlines()

    for line in lines:
        if not line.strip():
            continue

        try:
            body = json.loads(line)
            logging.info('Created body for response')
            data.append(body)        

        except Exception as e:
            logging.error(f'Failed extracting the response due to: {e}')
            traceback.print_exc()
            return None

    return data

def comments_section_extract(response):
    data = []

    try:
        raw_response = response.json()
        for res_key, res_val in raw_response.items():
            if res_key == "data":
                data.append(res_val)
    except Exception as e:
        logging.error(f'Failed extracting the response due to: {e}')
        traceback.print_exc()
        return None
    return data


EXTRACT_MAP = {
    "main_comment_load": main_comment_extract,
    "comments_section": comments_section_extract
}

def fb_req_detector(response):
    if FB_URL_API in response.url and response.status == 200:
        logging.info(f'Found FB graphql shape in request - {FB_URL_API}')
        return comment_extractor_entry(response)
    return None

def comment_extractor_entry(response):
    req_headers = response.request.headers
    if FB_HEADER_KEY in req_headers:
        for header_key, header_val in FB_HEADER_VALUES.items():
            if req_headers[FB_HEADER_KEY] == header_val:
                logging.info(f'Found a {header_key} header')
                logging.info(f'Found header value {header_val}, extracting data...')
                return {
                    "flag": header_key,
                    "data": EXTRACT_MAP[header_key](response)
                    }