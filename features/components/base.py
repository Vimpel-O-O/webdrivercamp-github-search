from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import requests


class Base:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(self.driver, 10)

    def find_element_on_page(self, locator):
        element = self.wait.until(EC.visibility_of_element_located((By.XPATH, locator)))
        return element

    def find_text_on_page(self, locator):
        text = self.wait.until(EC.visibility_of_element_located((By.XPATH, locator))).text
        return text

    def insert_text(self, text, locator, return_way=False):
        element = self.find_element_on_page(locator)
        element.send_keys(text)

        if return_way:
            element.send_keys(Keys.RETURN)

    def click_item(self, locator):
        element = self.find_element_on_page(locator)
        element.click()

