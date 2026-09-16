import tkinter as tk
import threading
import sys
import logging
import traceback
from ui.text_redirector import TextRedirector
from fetcher.fetcher import Fetcher

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

class UI:

    stop_event: threading.Event

    def __init__(self):
        logging.info("Starting app")
        try:
            window = tk.Tk()
            window.title("Abyss Glancer - Fetcher")
            window.geometry("600x400")

            # The log viewing window
            log_box = tk.Text(window, bg="black", fg="green")
            log_box.pack(expand=True, fill="both", padx=10, pady=10)

            # Redirect terminal logs into the magic box
            sys.stdout = TextRedirector(log_box)
            sys.stderr = TextRedirector(log_box)
            logging.getLogger().addHandler(logging.StreamHandler(sys.stdout))
            logging.getLogger().setLevel(logging.INFO)

            self.stop_event = threading.Event()

            # Simple UI buttons
            btn_frame = tk.Frame(window)
            btn_frame.pack(pady=5)
            tk.Button(btn_frame, text="Start Fetcher", command=self.start_fetch, bg="lightgreen").pack(side="left", padx=10)
            tk.Button(btn_frame, text="Stop Gracefully", command=self.stop_fetch, bg="salmon").pack(side="left", padx=10)
            window.mainloop()

        except Exception as e:
            logging.error(f"Error starting app because - {e}")
            traceback.print_exc()

    def start_fetch(self):
        logging.info("Starting background worker...")
        fetcher = Fetcher()
        # Hire background thread so UI does not freeze![cite: 2]
        t = threading.Thread(target=fetcher.start_watcher, args=(self.stop_event,), daemon=True)
        t.start()

    def stop_fetch(self):
        logging.info("Stopping fetcher...")
        self.stop_event.set()