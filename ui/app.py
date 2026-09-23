import tkinter as tk
from tkinter import ttk
import threading
import sys
import logging
import traceback
from ui.buttons import BUTTONS
from ui.text_redirector import TextRedirector
from fetcher.fetcher import Fetcher
from api.sender import Sender

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

class UI:

    def __init__(self):
        logging.info("Starting app")

        try:
            self.window = tk.Tk()
            self.window.title("Abyss Glancer - Fetcher")
            self.window.geometry("1200x800")

            # The log viewing window
            self.log_box = tk.Text(self.window, bg="black", fg="green")
            self.log_box.pack(expand=True, fill="both", padx=10, pady=10)

            # Redirect terminal logs into the magic box
            sys.stdout = TextRedirector(self.log_box)
            sys.stderr = TextRedirector(self.log_box)
            logging.getLogger().addHandler(logging.StreamHandler(sys.stdout))
            logging.getLogger().setLevel(logging.INFO)

            self.stop_event = threading.Event()

            # Simple UI buttons
            self.btn_frame = tk.Frame(self.window)
            self.btn_frame.pack(pady=5)
            self.create_buttons()
            self.window.mainloop()

        except Exception as e:
            logging.error(f"Error starting app because - {e}")
            traceback.print_exc()

    def create_buttons(self):

        for button in BUTTONS:
            setattr(
                self, 
                button["name"],
                tk.Button(
                    self.btn_frame, 
                    text=button["title"], 
                    command=getattr(self, button["method"]), 
                    bg=button["bg"])
            )
            if button.get("disabled"):
                getattr(self, button["name"]).config(state=tk.DISABLED)
            getattr(self, button["name"]).pack(side=button["pack_side"], padx=10)
        

    def start_fetch(self):
        logging.info("Starting Fetcher worker...")
        self.fetcher = Fetcher()
        # Hire background thread so UI does not freeze![cite: 2]
        t = threading.Thread(target=self.fetcher.start_watcher, args=(self.stop_event,), daemon=True)
        t.start()

    def stop_fetch(self):
        logging.info("Stopping fetcher...")
        self.stop_event.set()

    def init_sender(self):
        logging.info("Starting Sender woker...")
        self.sender = Sender()
        if getattr(self, "sender", None):
            self.check_sender_enabled()

    def start_sender(self):
        logging.info("Sender is sending...")
        t = threading.Thread(
            target=self.sender.send_comments_for_analysis, 
            args=(
                getattr(self, "start_sender_btn"),
            ),
            daemon=True

        )
        t.start()

    def store_sender_results(self):
        logging.info("Storting Sender results...")
        t = threading.Thread(
            target=self.sender.save_roberta_scores, 
            args=(
                getattr(self, "store_sender_btn"),
            ),
            daemon=True)
        t.start()
        
    def check_sender_enabled(self):
        logging.info("Checking for sender...")
        if getattr(self.sender, "comment_data", None):
            for button in BUTTONS:
                if button.get("disabled"):
                    getattr(
                        self,
                        button["name"]
                    ).config(state=tk.NORMAL)
                    button["disabled"] = False
                    logging.info(f"Button for: {button.get("title")} enabled")