import logging
from selenium import webdriver
from constants import LOG_NAME


def number_format(num):
    num = num.replace(' ', '').replace('(', '').replace(')', '').replace('-', '')
    if num.startswith('0'):
        num = '38' + num
    return num


def timer(start, end):
    hours, rem = divmod(end-start, 3600)
    minutes, seconds = divmod(rem, 60)
    return "{:0>2}:{:0>2}:{:05.2f}".format(int(hours), int(minutes), seconds)


def webdriver_call():
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--incognito")
    chrome_options.add_argument("--headless")
    driver = webdriver.Chrome(chrome_options=chrome_options)
    driver.maximize_window()
    return driver


def logger_call():
    """ Configure our logger """

    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)

    formatter = logging.Formatter(
        '%(asctime)s - %(module)s: %(lineno)d\t%(levelname)s - '
        '%(threadName)s:\t%(message)s',
        datefmt='%m/%d/%Y %H:%M:%S'
    )

    # Save log to file
    file_handler = logging.FileHandler(LOG_NAME)
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(formatter)

    # Show log in console
    stream_handler = logging.StreamHandler()
    stream_handler.setLevel(logging.INFO)
    stream_handler.setFormatter(formatter)

    logger.addHandler(file_handler)
    logger.addHandler(stream_handler)
    return logger


class ElementHasAttribute(object):
    """An expectation for checking that an element has a particular attribute.

    returns the WebElement once it has the particular attribute
    """

    def __init__(self, locator, attribute_name, attribute_value):
        self.locator = locator
        self.attribute_name = attribute_name
        self.attribute_value = attribute_value

    def __call__(self, driver):
        # Finding the referenced element
        element = driver.find_element(*self.locator)

        if self.attribute_value in element.get_attribute(self.attribute_name):
            return element
        else:
            return False
