from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def get_pages(driver):
    # Scrape the total number of pages
    total_pages_text = driver.find_elements(By.CSS_SELECTOR, "ul.pagination li")[
        -2
    ].text
    return int(total_pages_text)


def scrape_links(driver):
    # max-w-full text-base
    a_tags = driver.find_elements(By.CSS_SELECTOR, "a.max-w-full.text-base")
    return [a_tag.get_attribute("href") for a_tag in a_tags]


def iterate_pages(driver):
    spinner = driver.find_element(By.CLASS_NAME, "animate-spin")
    WebDriverWait(driver, 10).until(EC.staleness_of(spinner))
    total_pages = get_pages(driver)
    links = []
    # Scrape the total number of pages
    total_pages_text = driver.find_elements(By.CSS_SELECTOR, "ul.pagination li")[
        -2
    ].text
    total_pages = int(total_pages_text)

    for current_page in range(2, total_pages + 1):
        # while current_page <= total_pages:

        WebDriverWait(driver, 10).until(EC.staleness_of(spinner))

        links.extend(scrape_links(driver))

        page_link = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable(
                (
                    By.XPATH,
                    f"//ul[contains(@class, 'pagination')]//li//span[text()='{current_page}']/..",
                )
            )
        )
        page_link.click()
        spinner = driver.find_element(By.CLASS_NAME, "animate-spin")

    return links
