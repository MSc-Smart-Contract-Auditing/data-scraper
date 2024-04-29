single = "https://etherscan.io/address/0x68bbed6a47194eff1cf514b50ea91895597fc91e#code"
multiple = (
    "https://etherscan.io/address/0x80fbb6122b8e023988e640db1ae348a10a7933e8#code"
)

from selenium import webdriver
from selenium.webdriver.common.by import By
import pyperclip
import time

driver = webdriver.Chrome()
# Loop
driver.get(multiple)

code_embedding = driver.find_element(By.ID, "dividcode")
source_code_block = code_embedding.find_elements(By.CSS_SELECTOR, "div.mb-4")[0]
copy_buttons = source_code_block.find_elements(
    By.XPATH, "//a[@aria-label='Copy source code to clipboard']"
)

for idx, button in enumerate(copy_buttons):
    driver.execute_script("arguments[0].scrollIntoView({block:'center'});", button)
    time.sleep(0.3)  # Wait for any lazy-loaded elements to stabilize
    button.click()
    code_content = pyperclip.paste()
    with open(f"verified/contracts/contract-{idx}.sol", "w") as file:
        file.write(code_content)

driver.quit()
