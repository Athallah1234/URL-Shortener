import tkinter as tk
from tkinter import ttk, scrolledtext, StringVar, filedialog
from pyshorteners import Shortener
import pyperclip
import webbrowser
import qrcode
import validators
import logging
import requests
import threading
import time

class URLShortenerApp:
    def __init__(self, master):
        self.master = master
        self.master.title("URL Shortener")
        self.click_counter = 0
        self.shortened_urls = []
        self.auto_refresh_enabled = False

        # Set up logging
        logging.basicConfig(filename='url_shortener.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

        # StringVar for dynamic error message
        self.error_message = StringVar()
        self.error_message.set("")

        # List to store URLs for auto-complete
        self.url_list = []

        self.create_widgets()

    def create_widgets(self):
        self.label_url = ttk.Label(self.master, text="Enter URL:")
        self.label_url.grid(row=0, column=0, pady=10, padx=10, sticky="w")

        # Entry widget with auto-complete
        self.entry_url = ttk.Combobox(self.master, width=50, values=self.url_list)
        self.entry_url.grid(row=0, column=1, pady=10, padx=10, sticky="ew")
        self.entry_url.bind("<FocusIn>", self.update_url_list)  # Update auto-complete list on focus

        self.btn_shorten = ttk.Button(self.master, text="Shorten", command=self.shorten_url)
        self.btn_shorten.grid(row=1, column=1, pady=10, padx=10, sticky="e")

        self.btn_expand = ttk.Button(self.master, text="Expand", command=self.expand_url)
        self.btn_expand.grid(row=1, column=2, pady=10, padx=10, sticky="e")

        self.label_result = ttk.Label(self.master, text="")
        self.label_result.grid(row=2, column=1, columnspan=2, pady=10, padx=10, sticky="w")

        # Dynamic error message label
        self.label_error = ttk.Label(self.master, textvariable=self.error_message, foreground="red")
        self.label_error.grid(row=3, column=1, columnspan=2, pady=10, padx=10, sticky="w")

        self.btn_copy_shortened = ttk.Button(self.master, text="Copy URL", command=self.copy_shortened_url)
        self.btn_copy_shortened.grid(row=4, column=1, columnspan=2, pady=10, padx=10, sticky="w")

        self.btn_open_browser = ttk.Button(self.master, text="Open in Browser", command=self.open_in_browser)
        self.btn_open_browser.grid(row=5, column=1, columnspan=2, pady=10, padx=10, sticky="w")

        self.label_click_counter = ttk.Label(self.master, text=f"Click Counter: {self.click_counter}")
        self.label_click_counter.grid(row=6, column=1, columnspan=2, pady=10, padx=10, sticky="w")

        self.btn_show_history = ttk.Button(self.master, text="Show History", command=self.show_history)
        self.btn_show_history.grid(row=7, column=1, columnspan=2, pady=10, padx=10, sticky="w")

        # New entry for generating QR code dynamically
        self.label_qr_url = ttk.Label(self.master, text="Enter URL for QR Code:")
        self.label_qr_url.grid(row=8, column=0, pady=10, padx=10, sticky="w")

        self.entry_qr_url = ttk.Entry(self.master, width=50)
        self.entry_qr_url.grid(row=8, column=1, pady=10, padx=10, sticky="ew")

        self.btn_generate_qr = ttk.Button(self.master, text="Generate QR Code", command=self.generate_qr_code)
        self.btn_generate_qr.grid(row=8, column=2, pady=10, padx=10, sticky="e")

        # New checkbox for enabling auto-refresh
        self.chk_auto_refresh = ttk.Checkbutton(self.master, text="Auto-Refresh URL", command=self.toggle_auto_refresh)
        self.chk_auto_refresh.grid(row=9, column=1, columnspan=2, pady=10, padx=10, sticky="w")

        # Start a thread for auto-refresh
        self.auto_refresh_thread = threading.Thread(target=self.auto_refresh_thread_function)
        self.auto_refresh_thread.daemon = True
        self.auto_refresh_thread.start()

    def update_url_list(self, event):
        # Update the auto-complete list when the entry widget gains focus
        self.url_list = list(set(self.url_list))  # Remove duplicates
        self.entry_url['values'] = self.url_list

    def validate_url(self, url):
        return validators.url(url)
    
    def clear_errors(self):
        # Clear error messages
        self.error_message.set("")
        self.label_result.config(text="", foreground="black")

    def shorten_url(self):
        original_url = self.entry_url.get()

        # Clear previous error messages
        self.clear_errors()

        if original_url:
            if self.validate_url(original_url):
                try:
                    s = Shortener()
                    shortened_url = s.tinyurl.short(original_url)
                    self.label_result.config(text=f"Original URL: {original_url}\nShortened URL: {shortened_url}", foreground="green")
                    self.shortened_urls.append((original_url, shortened_url))
                    self.shortened_url = shortened_url
                    logging.info(f"URL shortened: {original_url} -> {shortened_url}")

                    # Add the original URL to the auto-complete list
                    self.url_list.append(original_url)
                    self.update_url_list(None)
                except Exception as e:
                    error_message = f"Error shortening URL: {str(e)}"
                    self.label_result.config(text=error_message, foreground="red")
                    self.error_message.set(error_message)
                    logging.error(error_message)
            else:
                error_message = "Invalid URL. Please enter a valid URL."
                self.label_result.config(text=error_message, foreground="red")
                self.error_message.set(error_message)
                logging.warning(f"Invalid URL entered: {original_url}")
        else:
            error_message = "Please enter a URL"
            self.label_result.config(text=error_message, foreground="red")
            self.error_message.set(error_message)
            logging.warning("Empty URL entered")

    def expand_url(self):
        original_url = self.entry_url.get()

        # Clear previous error messages
        self.clear_errors()

        if original_url:
            if self.validate_url(original_url):
                try:
                    s = Shortener()
                    shortened_url = s.tinyurl.short(original_url)
                    response = requests.head(shortened_url, allow_redirects=True)
                    expanded_url = response.url
                    self.label_result.config(text=f"Shortened URL: {shortened_url}\nExpanded URL: {original_url}", foreground="blue")
                    logging.info(f"URL expanded: {original_url} -> {expanded_url}")
                except requests.RequestException as e:
                    error_message = f"Error expanding URL: {str(e)}"
                    self.label_result.config(text=error_message, foreground="red")
                    self.error_message.set(error_message)
                    logging.error(error_message)
                except Exception as e:
                    error_message = f"An unexpected error occurred: {str(e)}"
                    self.label_result.config(text=error_message, foreground="red")
                    self.error_message.set(error_message)
                    logging.error(error_message)
            else:
                error_message = "Invalid URL. Please enter a valid URL."
                self.label_result.config(text=error_message, foreground="red")
                self.error_message.set(error_message)
                logging.warning(f"Invalid URL entered: {original_url}")
        else:
            error_message = "Please enter a URL"
            self.label_result.config(text=error_message, foreground="red")
            self.error_message.set(error_message)
            logging.warning("Empty URL entered")

    def copy_shortened_url(self):
        if hasattr(self, 'shortened_url'):
            pyperclip.copy(self.shortened_url)
            self.label_result.config(text="URL copied to clipboard", foreground="blue")
            logging.info("URL copied to clipboard")
        else:
            error_message = "No URL available"
            self.label_result.config(text=error_message, foreground="red")
            self.error_message.set(error_message)
            logging.warning("Attempted to copy URL, but none available")

    def open_in_browser(self):
        if hasattr(self, 'shortened_url'):
            if self.validate_url(self.shortened_url):
                webbrowser.open(self.shortened_url)
                self.click_counter += 1
                self.label_click_counter.config(text=f"Click Counter: {self.click_counter}")
                self.label_result.config(text="Opened in default browser", foreground="blue")
                logging.info(f"URL opened in browser: {self.shortened_url}")
            else:
                error_message = "Invalid URL. Cannot open in browser."
                self.label_result.config(text=error_message, foreground="red")
                self.error_message.set(error_message)
                logging.warning(f"Invalid URL for opening in browser: {self.shortened_url}")
        else:
            error_message = "No URL available"
            self.label_result.config(text=error_message, foreground="red")
            self.error_message.set(error_message)
            logging.warning("Attempted to open URL in browser, but none available")

    def generate_qr_code(self):
        input_url = self.entry_qr_url.get()

        # Clear previous error messages
        self.clear_errors()

        if input_url:
            if self.validate_url(input_url):
                qr = qrcode.QRCode(
                    version=1,
                    error_correction=qrcode.constants.ERROR_CORRECT_L,
                    box_size=10,
                    border=4,
                )
                qr.add_data(input_url)
                qr.make(fit=True)

                qr_image = qr.make_image(fill_color="black", back_color="white")

                qr_image.show()

                self.label_result.config(text="QR Code generated", foreground="blue")
                logging.info("QR Code generated")
            else:
                error_message = "Invalid URL. Cannot generate QR Code."
                self.label_result.config(text=error_message, foreground="red")
                self.error_message.set(error_message)
                logging.warning("Attempted to generate QR Code, but invalid URL available")
        else:
            error_message = "Please enter a URL for QR Code generation"
            self.label_result.config(text=error_message, foreground="red")
            self.error_message.set(error_message)
            logging.warning("Attempted to generate QR Code without entering a URL")

    def show_history(self):
        history_window = tk.Toplevel(self.master)
        history_window.title("URL Shortener History")

        history_text = scrolledtext.ScrolledText(history_window, wrap=tk.WORD, width=60, height=20)
        history_text.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

        for i, (original_url, shortened_url) in enumerate(self.shortened_urls, start=1):
            history_text.insert(tk.END, f"{i}. Original: {original_url}\n   Shortened: {shortened_url}\n\n")

        history_text.config(state=tk.DISABLED)

        btn_clear_history = ttk.Button(history_window, text="Clear History", command=self.clear_history)
        btn_clear_history.grid(row=1, column=0, pady=10)

        btn_export_history = ttk.Button(history_window, text="Export History", command=self.export_history)
        btn_export_history.grid(row=2, column=0, pady=10)

    def export_history(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt")])
        if file_path:
            with open(file_path, "w") as file:
                for i, (original_url, shortened_url) in enumerate(self.shortened_urls, start=1):
                    file.write(f"{i}. Original: {original_url}\n   Shortened: {shortened_url}\n\n")

            self.label_result.config(text=f"History exported to {file_path}", foreground="blue")
            logging.info(f"History exported to {file_path}")

    def clear_history(self):
        self.shortened_urls = []
        self.show_history()

    def toggle_auto_refresh(self):
        self.auto_refresh_enabled = not self.auto_refresh_enabled

    def auto_refresh_thread_function(self):
        while True:
            if self.auto_refresh_enabled and hasattr(self, 'shortened_url'):
                try:
                    response = requests.head(self.shortened_url, allow_redirects=True)
                    expanded_url = response.url
                    self.label_result.config(text=f"Auto-Refreshed URL: {expanded_url}", foreground="blue")
                    logging.info(f"Auto-Refreshed URL: {expanded_url}")
                except requests.RequestException as e:
                    error_message = f"Error auto-refreshing URL: {str(e)}"
                    self.label_result.config(text=error_message, foreground="red")
                    self.error_message.set(error_message)
                    logging.error(error_message)
            time.sleep(60)  # Auto-refresh every 60 seconds

if __name__ == "__main__":
    root = tk.Tk()
    app = URLShortenerApp(root)
    root.mainloop()

