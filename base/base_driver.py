# In this file is the commom methods that will be reused several times in various test classes

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait


class BaseDriver:
    def __init__(self, driver):
        self.driver = driver

    def wait_for(self, seconds):
        wait = WebDriverWait(self.driver, seconds)
        w = wait
        return w

    def wait_for_presence_of_all_elements(self, locator):
        list_of_elements = self.wait_for(5).until(EC.presence_of_element_located((By.CSS_SELECTOR, locator)))
        return list_of_elements

    def wait_for_visibility_of_element(self, locator):
        element = self.wait_for(5).until(EC.visibility_of_element_located((By.CSS_SELECTOR, locator)))
        return element

    def wait_for_element_to_be_clickable(self, locator):
        element = self.wait_for(5).until(EC.element_to_be_clickable((By.CSS_SELECTOR, locator)))
        return element

    def wait_for_invisible_of_element(self, locator):
        element = self.wait_for(5).until(EC.invisibility_of_element_located((By.CSS_SELECTOR, locator)))
        return element