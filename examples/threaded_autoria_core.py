from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from math import ceil
from threading import Thread

from constants import (RIA_PATH, RIA_RESULTS, RIA_TICKETS, RIA_NAME,
                       RIA_PROFILE, RIA_NUMBER, RIA_PRICE, RIA_ADDRESS,
                       RIA_DESCRIPTION)
from database import insert_into_table, is_not_phone_exists
from helpers import logger_call

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--incognito")
chrome_options.add_argument("--headless")
driver = webdriver.Chrome(chrome_options=chrome_options)

logger = logger_call()


class ThreadLinks(Thread):
    def __init__(self):
        Thread.__init__(self)

    def run(self):    # Gather ticket links
        tickets_list = []
        driver.get(RIA_PATH)
        logger.info('Start piling the links...')
        ticket_num = int(driver.find_element(*RIA_RESULTS).text.replace(' ', ''))
        page_num = ceil(ticket_num / 100)

        for page in range(page_num):
            driver.get(f'{RIA_PATH}&page={page}')
            for ticket in driver.find_elements(*RIA_TICKETS):
                tickets_list.append(ticket.get_attribute('href'))
        logger.info(f'Links are gathered. There are {len(tickets_list)} in total')

    def get_links():
        """Gather ticket links"""
        for page in range(page_num):
            driver.get(f'{RIA_PATH}&page={page}')
            for ticket in driver.find_elements(*RIA_TICKETS):
                tickets_list.append(ticket.get_attribute('href'))
        driver.close()


class ThreadData(Thread):
    def __init__(self):
        Thread.__init__(self)

    def run(self, tickets_list):     # Gather data from tickets
        logger.info('Start looping through the links...')
        for ticket in tickets_list:
            driver.get(ticket)
            logger.info(f'Checking link: {ticket}')

            try:    # Get number(s)
                phone_numbers = driver.find_elements(*RIA_NUMBER)
                numbers = []
                for number in phone_numbers:
                    if number.tag_name == 'span':
                        numbers.append(number.get_attribute('data-phone-number'))
                numbers = '\n'.join(numbers)
            except NoSuchElementException:
                logger.debug(f'No numbers found in link {ticket}.')
                continue

            if is_not_phone_exists(numbers):
                logger.info(
                    f'Found unique number. Gathering info from link {ticket}...')
                try:
                    profile = driver.find_element(*RIA_PROFILE) \
                        .find_element_by_tag_name('a').get_attribute('href')
                except NoSuchElementException:
                    profile = None

                insert_into_table(numbers,
                                  driver.find_element(*RIA_NAME).text,
                                  driver.current_url,
                                  driver.find_element(*RIA_PRICE).text,
                                  profile,
                                  driver.find_element(*RIA_DESCRIPTION).text,
                                  driver.find_element(*RIA_ADDRESS).text)
                logger.info(f'Information from {ticket} was stored in db.')
            else:
                logger.debug('Already in the base. Skip...')

        driver.close()
