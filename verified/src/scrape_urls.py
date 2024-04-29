from selenium import webdriver
from selenium.webdriver.common.by import By
from .database import Database

db = Database()

driver = webdriver.Chrome()

pages = 5

for page in range(1, pages + 1):
    driver.get(f"https://etherscan.io/contractsVerified/{page}?filter=audit&ps=100")
    table = driver.find_element(By.CSS_SELECTOR, ".align-middle.text-nowrap")
    rows = table.find_elements(By.TAG_NAME, "tr")
    db.addElementsAndFilter(rows)

db.save()

driver.quit()
