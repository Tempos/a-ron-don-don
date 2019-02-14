import threading
from queue import Queue
from time import time
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from math import ceil
from constants import (RIA_PATH, RIA_RESULTS, RIA_TICKETS, RIA_NAME,
                       RIA_PROFILE, RIA_NUMBER, RIA_PRICE, RIA_ADDRESS,
                       RIA_DESCRIPTION)
from database import create_bd, insert_into_table, is_not_phone_exists
from helpers import logger_call

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--incognito")
chrome_options.add_argument("--headless")
driver = webdriver.Chrome(chrome_options=chrome_options)

create_bd()
logger = logger_call()

# Gather ticket links
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

print(f"Found {len(tickets_list)} links")

locker = threading.Lock()


def get_data(links):  # Gather data from tickets
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--incognito")
    chrome_options.add_argument("--headless")
    driver = webdriver.Chrome(chrome_options=chrome_options)
    
    with locker:
        logger.info('Start looping through the links...')
        for link in links:
            driver.get(link)
            print(f"Starting thread {threading.current_thread().name}. Checking link {link}")

        # try:  # Get number(s)
        #     phone_numbers = driver.find_elements(*RIA_NUMBER)
        #     numbers = []
        #     for number in phone_numbers:
        #         if number.tag_name == 'span':
        #             numbers.append(number.get_attribute('data-phone-number'))
        #     numbers = '\n'.join(numbers)
        # except NoSuchElementException:
        #     logger.debug(f'No numbers found in link {link}.')
        # print(numbers)

        # if is_not_phone_exists(numbers):
        #     logger.info(
        #         f'Found unique number. Gathering info from link {ticket}...')
        #     name = driver.find_element(*RIA_NAME).text
        #     address = driver.find_element(*RIA_ADDRESS).text
        #     price = driver.find_element(*RIA_PRICE).text
        #     try:
        #         profile = driver.find_element(*RIA_PROFILE) \
        #             .find_element_by_tag_name('a').get_attribute('href')
        #     except NoSuchElementException:
        #         profile = None
        #     info = driver.find_element(*RIA_DESCRIPTION).text
        #     link = driver.current_url
        #
        #     # insert_into_table(numbers, name, link, price, profile, info,
        #     #                   address)
        #     print(numbers, name, link, price, profile, info, address)
        #     logger.info(f'Information from {ticket} was stored in db.')
        # else:
        #     logger.debug('Already in the base. Skip...')
        driver.close()


def process_queue():
    while True:
        cur_url_list = Q.get()
        get_data(cur_url_list)


if __name__ == '__main__':
    Q = Queue()
    thread_num = 5

    for i in range(thread_num):
        t = threading.Thread(target=process_queue)
        t.daemon = True
        t.start()

    llc = [tickets_list[i:i + thread_num] for i in range(0,
                                                         len(tickets_list),
                                                         thread_num)]
    print(llc)

    start = time()
    for lst in llc:
        Q.put(lst)

    # Q.put(llc)
    Q.join()

    print(threading.enumerate())
    print(f"Execution time: {time()-start}")

    driver.close()
