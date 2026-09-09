import logging
from controller import analyze_comment
from storer.db_handler import DBHandler

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

class Sender:
    COLLAB_PUBLIC_URL = "https://fiscally-fox-carrot.ngrok-free.dev/evaluate"
    db_handler = DBHandler()
    comment_data: list[dict]
    analyzed_comments = list[list]
    op_results = {
        "successful": 0,
        "failed": 0
    }

    def __init__(self):
        logging.info("Setup for analysis of comment data inilializing...")

        comment_data = self.db_handler.un_analyzed_comments()

        logging.info(f"Found {len(comment_data)} comments to analyize")

    def send_comments_for_analysis(self):
        logging.info(f"Sending comments for analysis...")

        for comment in self.comment_data:
            logging.info(f"Sending comment id {comment.get("comment_id")} for analysis")
            result = analyze_comment(comment.get("comment_id"))
            if result:
                logging.info(f"Successfully received analysis for comment ✅")
                self.analyzed_comments.append(result)
                self.op_results.get("successful") += 1
                continue

            logging.error(f"ERROR - Comment was not analyzed ❌")
            self.op_results.get("failed") += 1

        logging.info(f"Successfully analyzed {self.op_results.get("successful")} comments")
        if self.op_results.get("failed") > 0:
            logging.error(f"Failed on {self.op_results.get("failed")} comments, please check the logs")
    


