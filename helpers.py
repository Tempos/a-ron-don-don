import logging
from constants import RIA_LOG_NAME


def number_format(num):
    num = num.replace(' ', '').replace('(', '').replace(')', '').replace('-', '')
    if num.startswith('0'):
        num = '38' + num
    return num


def logger_call():
    """ Configure our logger """

    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)

    formatter = logging.Formatter(
        '%(asctime)s -- %(module)s -- %(levelname)s -- %(message)s',
        datefmt='%m/%d/%Y %H:%M:%S')

    # Save log to file
    file_handler = logging.FileHandler(RIA_LOG_NAME)
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
        element = driver.find_element(*self.locator)  # Finding the referenced element
        if self.attribute_value in element.get_attribute(self.attribute_name):
            return element
        else:
            return False
