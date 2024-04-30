single = "https://etherscan.io/address/0x68bbed6a47194eff1cf514b50ea91895597fc91e#code"
multiple = (
    "https://etherscan.io/address/0x80fbb6122b8e023988e640db1ae348a10a7933e8#code"
)

from selenium import webdriver
from selenium.webdriver.common.by import By
import os
import pyperclip
import time
import re

driver = webdriver.Chrome()
# Loop
driver.get(multiple)

contract_name = driver.find_element(
    By.XPATH, "//div[text()='Contract Name:']/following-sibling::div/span"
).text

contract_directory = f"./contracts/{contract_name}"
os.makedirs(contract_directory, exist_ok=True)

code_embedding = driver.find_element(By.ID, "dividcode")
source_code_block = code_embedding.find_elements(By.CSS_SELECTOR, "div.mb-4")[0]
copy_buttons = source_code_block.find_elements(
    By.XPATH, "//a[@aria-label='Copy source code to clipboard']"
)

if len(copy_buttons) == 1:
    # File name is not present so default to contract name
    file_names = [contract_name]
else:
    # Scrape file names
    file_names = [
        re.sub(
            r"File\s\d+\sof\s\d+\s:\s",
            "",
            button.find_element(
                By.XPATH, "./ancestor::span/preceding-sibling::span"
            ).text,
        )
        for button in copy_buttons
    ]


for file_name, button in zip(file_names, copy_buttons):
    driver.execute_script("arguments[0].scrollIntoView({block:'center'});", button)
    time.sleep(0.3)  # Wait for any lazy-loaded elements to stabilize
    button.click()
    code_content = pyperclip.paste()
    with open(f"./contracts/{contract_name}/{file_name}", "w") as file:
        file.write(code_content)

driver.quit()
