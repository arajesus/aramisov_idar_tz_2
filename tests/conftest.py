import pytest
from driver import SetupDriver

from page_and_helpers.base_page import BasePage
from page_and_helpers.helper_user_generator import TestData


@pytest.fixture(scope="function")
def page_helper():
    return BasePage(SetupDriver.setup_driver())


@pytest.fixture(scope="function")
def test_data():
    return TestData()
