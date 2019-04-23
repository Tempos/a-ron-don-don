"""Threaded version of autoria.py"""

from threading import Thread, active_count
from queue import Queue
from selenium.common.exceptions import NoSuchElementException
from math import ceil
from helpers import logger_call, webdriver_call
from database import insert_into_table, is_not_phone_exists, link_exists
from constants import (RIA_PATH, RIA_RESULTS, RIA_TICKETS, RIA_NAME,
                       RIA_PROFILE, RIA_NUMBER, RIA_PRICE, RIA_ADDRESS,
                       RIA_DESCRIPTION)

logger = logger_call()
queue_in, queue_out = Queue(), Queue()


def get_links():
    """Gather ticket links"""

    driver = webdriver_call()

    driver.get(RIA_PATH)
    ticket_num = int(driver.find_element(*RIA_RESULTS).text.replace(' ', ''))
    page_num = ceil(ticket_num / 100)

    for page in range(page_num):
        driver.get(f'{RIA_PATH}&page={page}')
        for ticket in driver.find_elements(*RIA_TICKETS):
            url = ticket.get_attribute('href')
            if not link_exists(url):
                queue_in.put(url)

    logger.info(f"Found {queue_in.qsize()} links")
    driver.close()


class GetData(Thread):
    """Gather data from links"""

    def __init__(self, q_in, q_out, driver=None):
        Thread.__init__(self)
        self.driver = driver if driver else webdriver_call()
        self.queue_in = q_in
        self.queue_out = q_out

    def run(self):
        logger.info("Started")

        while not self.queue_in.empty():
            ticket = self.queue_in.get()
            self.driver.get(ticket)

            try:    # Get number(s)
                numbers = []
                phone_numbers = self.driver.find_elements(*RIA_NUMBER)
                for number in phone_numbers:
                    if number.tag_name == 'span':
                        numbers.append(
                            number.get_attribute('data-phone-number'))
                numbers = '\n'.join(numbers)
            except NoSuchElementException:
                logger.debug(f'No numbers found in link {ticket}.')
                continue

            try:    # Get profile link
                profile = self.driver.find_element(*RIA_PROFILE)\
                    .find_element_by_tag_name('a').get_attribute('href')
            except NoSuchElementException:
                profile = None

            self.queue_out.put(
                (numbers,
                 self.driver.find_element(*RIA_NAME).text,
                 self.driver.current_url,
                 self.driver.find_element(*RIA_PRICE).text,
                 profile,
                 self.driver.find_element(*RIA_DESCRIPTION).text,
                 self.driver.find_element(*RIA_ADDRESS).text)
            )
            logger.debug(f"Data was put in queue - Link: {ticket} ")
            self.queue_in.task_done()

        logger.info("Finished.")
        self.driver.close()


class StoreData(Thread):
    """ Store unique data in DB"""

    def __init__(self, q_out):
        Thread.__init__(self)
        self.queue_out = q_out

    def run(self):
        while not self.queue_out.empty() or active_count() > 1:
            stored_data = self.queue_out.get()

            if is_not_phone_exists(stored_data[0]):
                logger.info("Found unique number. Storing info in db...")
                insert_into_table(*stored_data)
            else:
                logger.info('Already in the base. Skip...')

            self.queue_out.task_done()

        logger.info("Finished")
