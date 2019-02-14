from selenium import webdriver
from math import ceil
from threading import Thread
from queue import Queue
import datetime

from constants import (RIA_PATH, RIA_RESULTS, RIA_TICKETS, RIA_NAME,
                       RIA_PROFILE, RIA_NUMBER, RIA_PRICE, RIA_ADDRESS,
                       RIA_DESCRIPTION)
from helpers import logger_call

logger = logger_call()


class ThreadClass(Thread):
    def __init__(self, pagelist, queue):
        Thread.__init__(self)
        self.queue = queue
        self.pagelist = pagelist

    def run(self):
        now = datetime.datetime.now()
        print(f"{self.getName()} says Hello World at time: {now}")
        self.get_links(self.pagelist)

    def get_links(self):
        """Gather ticket links"""
        chr_opts = webdriver.ChromeOptions()
        chr_opts.add_argument("--incognito")
        chr_opts.add_argument("--headless")
        driver_tx = webdriver.Chrome(chrome_options=chr_opts)

        for ticket in self.pagelist:
            tickets_list.append(ticket.get_attribute('href'))
            print(ticket.get_attribute('href'))
        driver_tx.close()


if __name__ == '__main__':
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--incognito")
    chrome_options.add_argument("--headless")
    driver = webdriver.Chrome(chrome_options=chrome_options)

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

    pages_list = [driver.get(f'{RIA_PATH}&page={page}') for page in range(page_num)]

    for i in range(2):
        t = ThreadClass()
        t.start()
        t.join()
