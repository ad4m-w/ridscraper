# Open Table RID Scraper
# By Adam Waszczyszak

import os
import sys
import re
import csv
from tkinter import Tk, filedialog, Button, Label, StringVar, Entry
from tkinter import messagebox
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from pathlib import Path

def run_script(input_csv_path):

    options = Options()
    options.add_argument("--disable-gpu") 
    options.add_argument("--no-sandbox") 
    if getattr(sys, 'frozen', False):
        bundle_dir = Path(sys._MEIPASS) 
    else:
        bundle_dir = Path(os.path.abspath(os.path.dirname(__file__)))

    chrome_binary = r'C:/Program Files/Google/Chrome/Application/chrome.exe'
    chromedriver_path = bundle_dir / 'chromedriver.exe'

    options.binary_location = chrome_binary

    if not chromedriver_path.exists():
        messagebox.showerror("Error", "chromedriver.exe not found!")
        return

    service = Service(str(chromedriver_path))
    driver = webdriver.Chrome(service=service, options=options)

    output_csv_path = os.path.splitext(input_csv_path)[0] + '_output.csv'

    try:
        with open(input_csv_path, mode='r', newline='', encoding='utf-8') as infile:
            csvreader = csv.reader(infile)
            rows = list(csvreader)

            with open(output_csv_path, mode='w', newline='', encoding='utf-8') as outfile:
                csvwriter = csv.writer(outfile)

                header = rows[0]
                if header[0] != 'Link' or header[1] != 'RID':
                    header = ['Link', 'RID']
                csvwriter.writerow(header)

                for row in rows[1:]:
                    link = row[0]
                    if link:
                        driver.get(link)
                        page_source = driver.page_source
                        match = re.search(r'rid=(\d+)', page_source)

                        if match:
                            rid = match.group(1)
                        else:
                            rid = 'RID not found'

                        csvwriter.writerow([link, rid])

        messagebox.showinfo("Success", f'Scraped links and saved RIDs to {output_csv_path}')
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {str(e)}")
    finally:
        driver.quit()

def browse_file():
    file_path = filedialog.askopenfilename(title="Select CSV file", filetypes=[("CSV Files", "*.csv")])
    if file_path:
        input_csv_var.set(file_path)

def on_submit():
    input_csv_path = input_csv_var.get()
    if not input_csv_path:
        messagebox.showwarning("Warning", "Please select a CSV file first.")
    else:
        run_script(input_csv_path)

root = Tk()
root.title("adamwasz.com")
Label(root, text="Browse for a CSV file to process:").grid(row=0, column=0, padx=10, pady=10)
input_csv_var = StringVar()
entry_file = Entry(root, textvariable=input_csv_var, width=50)
entry_file.grid(row=1, column=0, padx=10, pady=10)
Button(root, text="Browse", command=browse_file).grid(row=1, column=1, padx=10, pady=10)
Button(root, text="Submit", command=on_submit).grid(row=2, column=0, columnspan=2, padx=10, pady=10)
root.mainloop()