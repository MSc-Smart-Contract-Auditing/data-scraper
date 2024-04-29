from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from tqdm import tqdm

from .helpers.validation_exception import ValidationException
from .helpers.setup import setup
from .database import Database

import argparse
import json

parser = argparse.ArgumentParser(description="Scrape links from a source.")
parser.add_argument(
    "-s", "--source", type=str, required=True, help="The source to scrape from"
)
args = parser.parse_args()

if args.source == "Cyfrin":
    from .parsers.cyfrin_parser import parse_markdown_elements
elif args.source == "Codehawks":
    from .parsers.codehawks_parser import parse_markdown_elements
elif args.source == "ConsenSys":
    from .parsers.consensys_parser import parse_markdown_elements
else:
    print("Unknown source")
    exit(1)

# Open the JSON file for reading
with open("account.json", "r") as file:
    login_details = json.load(file)

# Load {source}.csv
with open(f"{args.source}-urls.csv", "r") as file:
    urls = file.readlines()

db = Database(args.source)

# Setup WebDriver (make sure to have the correct driver for your browser, e.g., chromedriver)
driver = webdriver.Chrome()

setup(driver, login_details)

for url in tqdm(urls):
    driver.get(url)

    """
    Extract Name
    """
    name = (
        WebDriverWait(driver, 10)
        .until(EC.presence_of_element_located((By.CSS_SELECTOR, "span.text-2xl")))
        .text
    )

    """
    Extract Severity
    """
    severity = (
        WebDriverWait(driver, 10)
        .until(
            EC.presence_of_element_located(
                (By.CSS_SELECTOR, "span.text-xs.mx-auto.text-center")
            )
        )
        .text.lower()
    )
    """
    Extract Markdown
    """

    markdown_div = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "div.p-4.h-full.break-words"))
    )

    child_elements = markdown_div.find_elements(
        By.XPATH, ".//div[contains(@class, 'wmde-markdown')]/*"
    )

    try:
        sections = parse_markdown_elements(child_elements)
    except ValidationException as e:
        continue

    sections["name"] = name
    sections["severity"] = severity

    db.record(sections)

driver.quit()
