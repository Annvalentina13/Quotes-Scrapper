import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import requests
from bs4 import BeautifulSoup
import pandas as pd

class QuotesScraperApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Quotes Scraper")
        self.root.geometry("700x500")
        self.quotes_data = []

        # GUI Layout
        self.setup_gui()

    def setup_gui(self):
        title = tk.Label(self.root, text="Quotes Scraper", font=("Arial", 20), fg="white", bg="#3e3e3e")
        title.pack(pady=10, fill=tk.X)

        self.status = tk.Label(self.root, text="Status: Ready", font=("Arial", 12), anchor="w")
        self.status.pack(fill=tk.X, padx=10)

        btn_frame = tk.Frame(self.root)
        btn_frame.pack(pady=10)

        scrape_btn = tk.Button(btn_frame, text="Start Scraping", command=self.scrape_quotes)
        scrape_btn.grid(row=0, column=0, padx=10)

        export_csv_btn = tk.Button(btn_frame, text="Export to CSV", command=self.export_csv)
        export_csv_btn.grid(row=0, column=1, padx=10)

        export_json_btn = tk.Button(btn_frame, text="Export to JSON", command=self.export_json)
        export_json_btn.grid(row=0, column=2, padx=10)

        # Treeview to display scraped data
        self.tree = ttk.Treeview(self.root, columns=("Quote", "Author", "Tags"), show="headings")
        self.tree.heading("Quote", text="Quote")
        self.tree.heading("Author", text="Author")
        self.tree.heading("Tags", text="Tags")
        self.tree.pack(expand=True, fill=tk.BOTH, padx=10, pady=10)

    def scrape_quotes(self):
        self.status.config(text="Status: Scraping in progress...")
        self.root.update_idletasks()

        self.quotes_data.clear()
        self.tree.delete(*self.tree.get_children())

        base_url = "http://quotes.toscrape.com/page/{}/"
        for page in range(1, 11):
            url = base_url.format(page)
            response = requests.get(url)

            if "No quotes found!" in response.text:
                break

            soup = BeautifulSoup(response.text, "html.parser")
            quotes = soup.find_all("div", class_="quote")

            for quote in quotes:
                text = quote.find("span", class_="text").get_text()
                author = quote.find("small", class_="author").get_text()
                tags = [tag.get_text() for tag in quote.find_all("a", class_="tag")]
                data = {"Quote": text, "Author": author, "Tags": ", ".join(tags)}
                self.quotes_data.append(data)
                self.tree.insert("", "end", values=(text[:80] + "...", author, ", ".join(tags)))

        self.status.config(text=f"Status: Scraping complete. {len(self.quotes_data)} quotes found.")

    def export_csv(self):
        if not self.quotes_data:
            messagebox.showwarning("No Data", "Please scrape some quotes first.")
            return
        file_path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV Files", "*.csv")])
        if file_path:
            pd.DataFrame(self.quotes_data).to_csv(file_path, index=False, encoding="utf-8")
            messagebox.showinfo("Exported", f"Data exported to {file_path}")

    def export_json(self):
        if not self.quotes_data:
            messagebox.showwarning("No Data", "Please scrape some quotes first.")
            return
        file_path = filedialog.asksaveasfilename(defaultextension=".json", filetypes=[("JSON Files", "*.json")])
        if file_path:
            pd.DataFrame(self.quotes_data).to_json(file_path, orient="records", indent=4)
            messagebox.showinfo("Exported", f"Data exported to {file_path}")

if __name__ == "__main__":
    root = tk.Tk()
    app = QuotesScraperApp(root)
    root.configure(bg="#3e3e3e")
    root.mainloop()
