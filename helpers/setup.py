from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def get_div_by_label(driver, label):
    label = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located(
            (By.XPATH, f"//*[contains(text(), '{label}')]")
        )
    )
    return label.find_element(By.XPATH, "./parent::div")


def select_dropdown(driver, label, option):
    dropdown = get_div_by_label(driver, label)

    dropdown.click()

    items = dropdown.find_element(
        By.CSS_SELECTOR, ".my-react-select__menu.css-1nmdiq5-menu"
    )

    option = items.find_element(By.XPATH, f"//div[contains(text(), '{option}')]")
    option.click()


def search(driver):
    WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, f"//button[contains(text(), 'Search')]"))
    ).click()


def setup(driver, login_details):
    # Load random page to trigger the login screen
    driver.get("https://solodit.xyz/auth")

    """
    Login
    """

    email_input = driver.find_element(By.ID, "email")
    email_input.send_keys(login_details["email"])

    password_input = driver.find_element(By.ID, "password")
    password_input.send_keys(login_details["password"])

    login_button = driver.find_element(
        By.CSS_SELECTOR, "button.btn-primary.uppercase.px-10.mx-auto"
    )
    login_button.click()

    """
    Hide pop-ups
    """
    label = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located(
            (
                By.XPATH,
                "//label[contains(text(), 'Join 1400+ auditors in the Solodit community!')]",
            )
        )
    )

    close_button = label.find_element(By.XPATH, "./following-sibling::button")
    close_button.click()

    dismiss_button = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located(
            (By.XPATH, "//button[contains(text(), 'Dismiss')]")
        )
    )
    dismiss_button.click()


def adjust_filters(driver, source):
    select_dropdown(driver, "Impact", "LOW")
    select_dropdown(driver, "Source", source)
    search(driver)
