import time
from retry import retry

from selenium.webdriver.common.by import By
from selenium.webdriver import ActionChains, Keys
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException, StaleElementReferenceException

from locators.locators import navigate_locator, auth_locator, cybersports_page


HOST = 'https://dota2.ru/'


class BasePage:
    def __init__(self, driver):
        self.driver = driver
        self.url = HOST
        self.wait = WebDriverWait(driver, 3)
        self.action = ActionChains(driver)

    def close(self):
        self.driver.close()

    def open_by_url(self, url: str):
        """
        Метод открывает страницу
        :param url: страница
        """
        self.driver.get(url)
        return self

    def open_main_page(self, url: str = None):
        """
        Метод открывает страницу
        :param url: страница
        """
        url = url or self.url
        self.driver.get(url)
        if self.element_is_visible_bool(locator='//td/div/img[not(@id="svg")]'):
            self.move_to_element_and_click(locator='//td/div/img[not(@id="svg")]')

        self.element_is_visible(locator=navigate_locator['nav_item_by_name'].format("Киберспорт"))
        time.sleep(5)
        return self

    def auth_person(self, person: dict, clean: bool=False):
        """
        Метод авторизации
        """
        self.set_value(locator=auth_locator["login_input_form"], value=person["email"], clean=clean)
        self.set_value(locator=auth_locator["password_input_form"], value=person["password"], clean=clean)
        self.move_to_element_and_click(locator=auth_locator["submit_button_form"])
        if self.element_is_visible_bool(locator='//td/div/img[not(@id="svg")]'):
            self.move_to_element_and_click(locator='//td/div/img[not(@id="svg")]')
        time.sleep(2)
        return self

    @staticmethod
    def self_exception(err, locator=None):
        error = err.__class__.__name__

        match error:
            case 'InvalidSelectorException':
                raise Exception(f"Не валидный локатор {locator}")
            case "TimeoutException":
                raise Exception(f"Время ожидания вышло {locator}")
            case 'NoSuchElementException':
                raise Exception(f"Элемента нет на странице {locator}")
            case 'InvalidArgumentException':
                raise Exception(f"В метод передан не верный аргумент {locator}, возможно ожидали WebElement")
            case _:
                raise Exception("Неизвестная ошибка")

    @retry((TimeoutException, NoSuchElementException), tries=5, delay=2)
    def get_element_path(self, locator: str) -> WebElement:
        """
        Найти элемент
        :param locator
        :return: element
        """
        try:
            return self.driver.find_element(By.XPATH, value=locator)
        except (TimeoutException, NoSuchElementException) as err:
            BasePage.self_exception(err, locator)
        except BaseException as err:
            BasePage.self_exception(err, locator)

    def get_elements_path(self, locator):
        """
        Найти элементы
        :param locator
        :return: elements
        """
        try:
            self.wait.until(EC.presence_of_all_elements_located(locator=(By.XPATH, locator)))
            return self.driver.find_elements(By.XPATH, value=locator)
        except BaseException as err:
            self.self_exception(err, locator)

    def element_is_visible(self, locator):
        try:
            self.wait.until(EC.visibility_of_element_located(locator=(By.XPATH, locator)))
            return self
        except BaseException as err:
            self.self_exception(err, locator)

    def element_is_visible_bool(self, locator):
        try:
            self.wait.until(EC.visibility_of_element_located(locator=(By.XPATH, locator)))
            return True
        except TimeoutException:
            return False

    def move_to_element_and_click(self, locator: str):
        """Навести курсор на элемент и Нажать"""
        for _ in range(3):
            try:
                element = self.get_element_path(locator=locator)
                self.wait.until(EC.element_to_be_clickable((By.XPATH, locator)))
                self.action.move_to_element(to_element=element).click(element).perform()
                time.sleep(2)
                break
            except self.self_exception(locator=locator, err='Не удалось навести курсор на элемент и нажать'):
                continue
        else:
            raise StaleElementReferenceException("Элемент стал устаревшим (StaleElementReferenceException)")
        return self

    def get_text(self, locator) -> str:
        """Получить не пустой текст"""
        element = self.get_element_path(locator)
        text = element.text
        assert bool(text), "Текст пуст"
        return text

    def get_text_element(self, element: WebElement) -> str:
        """Получить текст элемента
        :return text
        """
        return element.text

    def set_value(self, locator, value, clean=False):
        if clean:
            self.get_element_path(locator=locator).clear()
        element = self.get_element_path(locator)
        element.send_keys(value)
        return self

    def clear_input(self, locator):
        """Очистить поле ввода"""
        for i in range(0, int(len(self.get_attribute_value(locator=locator, attribute_name='value'))) + 1):
            self.set_value(locator=locator, value=Keys.BACKSPACE)
            self.set_value(locator=locator, value=Keys.DELETE)
        return self

    def get_attribute_value(self, locator: str, attribute_name: str):
        """
        Получить значение атрибута locator для WebElement
        :param locator: xpath для WebElement
        :param attribute_name: название атрибута
        """
        element = self.get_element_path(locator)
        return element.get_attribute(attribute_name)

    def click_nav_item(self, nav_item_name: str):
        self.move_to_element_and_click(locator=navigate_locator['nav_item_by_name'].format(nav_item_name))
        if self.element_is_visible_bool(locator='//td/div/img[not(@id="svg")]'):
            self.move_to_element_and_click(locator='//td/div/img[not(@id="svg")]')

    def click_nav_item_cybersports(self, nav_item_name: str):
        self.move_to_element_and_click(locator=cybersports_page['nav_item_by_name'].format(nav_item_name))
        if self.element_is_visible_bool(locator='//td/div/img[not(@id="svg")]'):
            self.move_to_element_and_click(locator='//td/div/img[not(@id="svg")]')
