from selenium import webdriver
from selenium.webdriver.chrome.options import Options


class SetupDriver:

    @staticmethod
    def setup_driver(headless=False):
        options = Options()
        if headless:
            options.add_argument('--headless')

        driver = webdriver.Chrome(options=options)
        driver.maximize_window()
        return driver
