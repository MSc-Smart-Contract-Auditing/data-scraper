from selenium import webdriver
from selenium.webdriver.common.by import By
from tqdm import tqdm
from pathlib import Path
import os
import pyperclip
import time
import re
import csv

driver = webdriver.Chrome()


def read_csv(file_path):
    with open(file_path, mode="r") as csv_file:
        return [row for row in csv.DictReader(csv_file)]


# Example usage
file_path = "audited-urls.csv"
items = read_csv(file_path)


cookies = True
for item in tqdm(items):
    driver.get(item["url"])

    contract_name = driver.find_element(
        By.XPATH, "//div[text()='Contract Name:']/following-sibling::div/span"
    ).text

    # Close annoying pop-up
    if cookies:
        driver.find_element(By.ID, "btnCookie").click()
        cookies = False

    contract_directory = Path(f"contracts/{contract_name}-{item['compiler_version']}")
    os.makedirs(contract_directory, exist_ok=True)

    code_embedding = driver.find_element(By.ID, "dividcode")
    source_code_block = code_embedding.find_elements(By.CSS_SELECTOR, "div.mb-4")[0]
    copy_buttons = source_code_block.find_elements(
        By.XPATH, "//a[@aria-label='Copy source code to clipboard']"
    )

    if len(copy_buttons) == 1:
        # File name is not present so default to contract name
        file_names = [f"{contract_name}.sol"]
    else:
        # Scrape file names
        file_names = [
            re.sub(
                r"File\s\d+\sof\s\d+\s?:\s",
                "",
                button.find_element(
                    By.XPATH, "./ancestor::span/preceding-sibling::span"
                ).text,
            )
            for button in copy_buttons
        ]

    for file_name, button in zip(file_names, copy_buttons):
        driver.execute_script(
            "arguments[0].scrollIntoView({block: 'center'});",
            button,
        )
        time.sleep(0.5)
        button.click()
        code_content = pyperclip.paste()
        with open(contract_directory / file_name, "w") as file:
            file.write(code_content)

driver.quit()
