from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from helpers.validation_expection import ValidationException

from helpers.setup import setup
from helpers.parse import parse_markdown_elements

import argparse
import json

parser = argparse.ArgumentParser(description="Scrape links from a source.")
parser.add_argument(
    "-s", "--source", type=str, required=True, help="The source to scrape from"
)
args = parser.parse_args()

# Open the JSON file for reading
with open("account.json", "r") as file:
    login_details = json.load(file)

# Load {source}.csv
with open(f"{args.source}-urls.csv", "r") as file:
    urls = file.readlines()

# Setup WebDriver (make sure to have the correct driver for your browser, e.g., chromedriver)
driver = webdriver.Chrome()

setup(driver, login_details)


for url in urls:
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
        # print(e)
        continue

    print(f"URL: {url}")
    print(f"Name: {name}")
    print(f"Severity: {severity}")
    # print(f"Desctiption: {sections['description']}")
    print(f"Function: {sections['function']}")
    print("####################")
    print("\n\n")

    # Contact api to submit the data

driver.quit()
