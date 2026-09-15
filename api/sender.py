import logging, time
from storer.db_handler import DBHandler
from api.controller_api import analyze_comment
from api.global_vals import COLLAB_PUBLIC_URL

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

class Sender:
    db_handler = DBHandler()
    comment_data: list[dict]
    analyzed_comments = []
    op_results = {
        "successful": 0,
        "failed": 0
    }

    def __init__(self):
        logging.info("Setup for analysis of comment data inilializing...")

        self.comment_data = self.db_handler.un_analyzed_comments()

        logging.info(f"Found {len(self.comment_data)} comments to analyize")

    def send_comments_for_analysis(self):
        logging.info(f"Sending comments for analysis...")

        for comment in self.comment_data:
            logging.info(f"Sending comment id {comment.get("comment_id")} for analysis")
            result = analyze_comment(COLLAB_PUBLIC_URL, comment.get("comment_id"))
            if result:
                logging.info(f"Successfully received analysis for comment")
                self.analyzed_comments.append(result)
                self.op_results["successful"] += 1
                time.sleep(0.5)
                continue

            logging.error(f"ERROR - Comment was not analyzed")
            self.op_results["failed"] += 1

        logging.info(f"Successfully analyzed {self.op_results.get("successful")} comments")
        if self.op_results.get("failed") > 0:
            logging.error(f"Failed on {self.op_results.get("failed")} comments, please check the logs")

    def save_roberta_scores(self):

        for result in self.analyzed_comments:
            comment_id = result["comment"]
            raw_scores = result["roberta_scores"]

            self.db_handler.store_roberta_scores(comment_id, raw_scores)

        self.db_handler.terminate_connection()