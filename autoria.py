from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from math import ceil
from constants import (RIA_PATH, RIA_RESULTS, RIA_TICKETS, RIA_NAME,
                       RIA_PROFILE, RIA_NUMBER, RIA_PRICE, RIA_ADDRESS,
                       RIA_DESCRIPTION)
from database import create_bd, insert_into_table, is_not_phone_exists

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--incognito")
chrome_options.add_argument("--headless")
driver = webdriver.Chrome(chrome_options=chrome_options)
driver.maximize_window()

create_bd()

# Gather ticket links
tickets_list = []
driver.get(RIA_PATH)
ticket_num = int(driver.find_element(*RIA_RESULTS).text.replace(' ', ''))
page_num = ceil(ticket_num / 100)
for page in range(page_num):
    driver.get(f'{RIA_PATH}&page={page}')
    for ticket in driver.find_elements(*RIA_TICKETS):
        tickets_list.append(ticket.get_attribute('href'))

# Gather data from tickets
for ticket in tickets_list:
    driver.get(ticket)
    try:
        # Get number(s)
        phone_numbers = driver.find_elements(*RIA_NUMBER)
        numbers = []
        for number in phone_numbers:
            if number.tag_name == 'span':
                numbers.append(number.get_attribute('data-phone-number'))
        numbers = '\n'.join(numbers)
    except NoSuchElementException:
        continue

    if is_not_phone_exists(numbers):
        name = driver.find_element(*RIA_NAME).text
        address = driver.find_element(*RIA_ADDRESS).text
        price = driver.find_element(*RIA_PRICE).text
        try:
            profile = driver.find_element(*RIA_PROFILE) \
                .find_element_by_tag_name('a').get_attribute('href')
        except NoSuchElementException:
            profile = None
        info = driver.find_element(*RIA_DESCRIPTION).text
        link = driver.current_url

        insert_into_table(numbers, name, link, price, profile, info, address)

driver.close()
