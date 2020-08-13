import getpass
import time

from selenium import webdriver

from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException

from constants import *
from helpers import number_format
from database import get_all, insert_into_telegram, is_telegram_acount, create_bd_telegram

create_bd_telegram()

username = getpass.getuser()
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument(
    "--user-data-dir=C://Users/{}/AppData/Local/Google/Chrome/User Data".format(username))
driver = webdriver.Chrome(chrome_options=chrome_options)
driver.maximize_window()

wait = WebDriverWait(driver, 10)

driver.get(TELEGRAM_URL)
time.sleep(20)

for _line in get_all():
    for number in [number_format(item) for item in _line[0].split('\n')]:
        # ToDo check by Id
        if is_telegram_acount(number):
            continue

        try:
            # Addition of phone number
            print(number + '-' * 40)

            driver.find_element_by_xpath(MENU).click()
            wait.until(EC.visibility_of_element_located((By.XPATH, CONTACTS))).click()
            driver.find_element_by_xpath(NEW_CONTACT).click()

            actions = ActionChains(driver)
            actions.move_to_element(driver.find_element_by_xpath(FIRST_NAME))
            actions.click()
            actions.move_to_element(driver.find_element_by_xpath(PHONE_NUMBER))
            actions.click()
            actions.send_keys(number + Keys.ENTER)
            actions.perform()
            actions.reset_actions()

            # Error Verification
            try:
                wait_err = WebDriverWait(driver, 3)
                wait_err.until(EC.visibility_of_element_located((By.XPATH, ERROR_NOT_FOUND)))
                insert_into_telegram(number, 'Not found')
                driver.find_element_by_tag_name('body').send_keys(Keys.ESCAPE + Keys.ESCAPE + Keys.ESCAPE)
                continue
            except TimeoutException:
                try:
                    wait_err = WebDriverWait(driver, 1)
                    wait_err.until(EC.visibility_of_element_located((By.XPATH, ERROR_TOO_FAST)))
                    print('=' * 20 + 'Too fast' + '=' * 20)
                    time.sleep(140)
                    driver.find_element_by_tag_name('body').send_keys(Keys.ESCAPE + Keys.ESCAPE + Keys.ESCAPE)
                    continue
                except TimeoutException:
                    pass

            # Get name and time of visit
            wait.until(EC.visibility_of_element_located((By.XPATH, PROFILE))).click()
            driver.find_element_by_xpath(ACTION_MORE).click()
            wait.until(EC.visibility_of_element_located((By.XPATH, ACTION_DELETE_CONTACT))).click()

            # Removal Waiting
            try:
                WebDriverWait(driver, 3).until_not(
                    EC.presence_of_element_located((By.XPATH, ACTION_DELETE_CONTACT)))
            except TimeoutException:
                # Reopen profile
                driver.find_element_by_xpath(CLOSE).click()
                wait.until(EC.visibility_of_element_located((By.XPATH, PROFILE))).click()
                time.sleep(1)

            user_name = driver.find_element_by_xpath(PROFILE_NAME).text
            last_seen = driver.find_element_by_xpath(PROFILE_SEEN).text
            user_profile = None
            try:
                user_profile = driver.find_element_by_xpath(PROFILE_DESCRIPTION).text
            except:
                pass  # ignore

            insert_into_telegram(number, user_name, seen=last_seen, profile=user_profile)
            print(user_name)

            driver.find_element_by_xpath(CLOSE).click()
        except Exception as err:
            print(type(err))
        driver.find_element_by_tag_name('body').send_keys(Keys.ESCAPE + Keys.ESCAPE + Keys.ESCAPE)

driver.close()
