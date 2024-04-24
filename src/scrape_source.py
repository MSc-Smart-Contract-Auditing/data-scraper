import argparse
from selenium import webdriver
import json
import csv

from setup import setup, adjust_filters
from scrape import iterate_pages

parser = argparse.ArgumentParser(description="Scrape links from a source.")
parser.add_argument(
    "-s", "--source", type=str, required=True, help="The source to scrape from"
)
args = parser.parse_args()

with open("account.json", "r") as file:
    login_details = json.load(file)

driver = webdriver.Chrome()

setup(driver, login_details)
adjust_filters(driver, args.source)
links = iterate_pages(driver)
driver.quit()

"""
Save URLs
"""

with open(f"{args.source}.csv", "w", newline="", encoding="utf-8") as csvfile:
    link_writer = csv.writer(csvfile)
    for link in links:
        link_writer.writerow([link])
