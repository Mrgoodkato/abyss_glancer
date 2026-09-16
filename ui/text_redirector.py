import tkinter as tk

# 1. Magic Basket to catch print() and logging rocks, putting them in UI
class TextRedirector:
    def __init__(self, widget):
        self.widget = widget

    def write(self, text_string):
        self.widget.insert(tk.END, text_string)
        self.widget.see(tk.END) # Auto-scroll to bottom

    def flush(self):
        pass