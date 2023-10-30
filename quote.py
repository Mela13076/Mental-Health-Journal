import tkinter as tk
from tkinter import ttk
import json
import random
import time


def load(app):
    global quote_label

    quote_frame = ttk.LabelFrame(app, text="Inspirational Quote")
    quote_frame.grid(row=3, columnspan=3, padx=10, pady=10, sticky="nsew")

    # Quote Widget
    quote_label = tk.Label(quote_frame, text="")
    quote_label.grid(row=0, column=0, padx=10, pady=5, sticky="e") 


    # Function to update the quote in the frame
    def update_quote():
        try:
            with open("quote.json", "r") as file:
                quotes = json.load(file)
                random_quote = random.choice(quotes)
                quote_label.config(text=random_quote)
        except FileNotFoundError:
            quote_label.config(text="Quote file not found")

    # Initial update
    update_quote()

    # Function to periodically update the quote
    def periodic_update():
        while True:
            update_quote()
            app.update_idletasks()  # Update the GUI
            time.sleep(150)  # Sleep for 5 minutes (300 seconds)

    # Start a separate thread for periodic updates
    import threading
    update_thread = threading.Thread(target=periodic_update)
    update_thread.daemon = True
    update_thread.start()