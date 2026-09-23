import logging, time
from tkinter import Button, DISABLED, NORMAL
from storer.db_handler import DBHandler
from api.controller_api import analyze_comment
from api.global_vals import COLLAB_PUBLIC_URL

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

class Sender:

    def __init__(self):
        logging.info("Setup for analysis of comment data inilializing...")

        self.db_handler = DBHandler()
        self.comment_data: list[dict]
        self.analyzed_comments = []

        self.op_results = {
            "successful": 0,
            "failed": 0
        }
        
        self.comment_data = self.db_handler.un_analyzed_comments()

        logging.info(f"Found {len(self.comment_data)} comments to analyize")

    def send_comments_for_analysis(self, tk_btn: Button):
        logging.info(f"Sending comments for analysis...")
        tk_btn.config(state=DISABLED)
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

        tk_btn.config(state=NORMAL)

    def save_roberta_scores(self, tk_btn: Button):
        tk_btn.config(state=DISABLED)
        for result in self.analyzed_comments:
            comment_id = result["comment"]
            raw_scores = result["roberta_scores"]

            self.db_handler.store_roberta_scores(comment_id, raw_scores)

        self.db_handler.terminate_connection()
        tk_btn.config(state=NORMAL)