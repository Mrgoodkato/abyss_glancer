FB_URL_API = "api/graphql/"
FB_HEADER_KEY = "x-fb-friendly-name"
FB_HEADER_VALUES = {
    "main_comment_load": "CometSinglePostDialogContentQuery",
    "comments_section": "CommentsListComponentsPaginationQuery"
}

def main_comment_extract():
    pass

def comments_section_extract():
    pass

EXTRACT_MAP = {
    "main_comment_load": main_comment_extract,
    "comments_section": comments_section_extract
}

def fb_req_detector(response):
    if FB_URL_API in response.url and response.status == 200:
        return True
    return False

def comment_extractor_entry(req_headers):
    
    if FB_HEADER_KEY in req_headers:
        for k, v in FB_HEADER_VALUES.items():
            if req_headers[FB_HEADER_KEY] == v:
                EXTRACT_MAP[k]()