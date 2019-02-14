from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from math import ceil

import threading
from queue import Queue
import time

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


class Threader(threading.Thread):
    def __init__(self, thread_id, name, datalist):
        threading.Thread.__init__(self)
        self.threadID = thread_id
        self.name = name
        self.datalist = datalist

    def run(self):
        print("Starting " + self.name)
        thread_lock.acquire()   # Get lock to synchronize threads
        get_data(self.datalist)
        thread_lock.release()   # Free lock to release next thread


# Function for the thread
def get_data(linklist):  # Gather data from tickets
    logger.info('Start looping through the links...')
    for link in linklist:
        driver.get(link)
        logger.info(f'Checking link: {link}')

        try:  # Get number(s)
            phone_numbers = driver.find_elements(*RIA_NUMBER)
            numbers = []
            for number in phone_numbers:
                if number.tag_name == 'span':
                    numbers.append(number.get_attribute('data-phone-number'))
            numbers = '\n'.join(numbers)
        except NoSuchElementException:
            logger.debug(f'No numbers found in link {link}.')
            continue

        if is_not_phone_exists(numbers):
            logger.info(
                f'Found unique number. Gathering info from link {link}...')
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
            logger.info(f'Information from {link} was stored in db.')
        else:
            logger.debug('Already in the base. Skip...')


def process_data(threadName, q):
   while not exitFlag:
      queueLock.acquire()
         if not workQueue.empty():
            data = q.get()
            queueLock.release()
            print "%s processing %s" % (threadName, data)
         else:
            queueLock.release()
         time.sleep(1)


thread_list = ["Thread-1", "Thread-2", "Thread-3"]
name_list = ["One", "Two", "Three", "Four", "Five"]
queue_lock = threading.Lock()
work_queue = Queue(10)
threads = []
thread_id = 1

# Create new threads
for name in thread_list:
    t = Threader(thread_id, name, work_queue)
    t.start()
    threads.append(t)
    thread_id += 1

# Fill the queue
queue_lock.acquire()
for word in name_list:
    work_queue.put(word)
queue_lock.release()

# Wait for queue to empty
while not work_queue.empty():
    pass

# Notify threads it's time to exit
exitFlag = 1

# Wait for all threads to complete
for t in threads:
    t.join()
print("Exiting Main Thread")

driver.close()
