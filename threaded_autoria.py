from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from math import ceil
from constants import (RIA_PATH, RIA_RESULTS, RIA_TICKETS, RIA_NAME,
                       RIA_PROFILE, RIA_NUMBER, RIA_PRICE, RIA_ADDRESS,
                       RIA_DESCRIPTION)
from database import create_bd, insert_into_table, is_not_phone_exists
from helpers import logger_call
import logging
import threading
from multiprocessing import Pool, cpu_count

create_bd()
logger = logger_call()


def run_parallel_selenium_processes(datalist, selenium_func):

    pool = Pool()

    # max number of parallel process
    iteration_count = cpu_count()-1

    count_per_iteration = len(datalist) / float(iteration_count)

    for i in range(0, iteration_count):
        list_start = int(count_per_iteration * i)
        list_end = int(count_per_iteration * (i+1))
        pool.apply_async(selenium_func, [datalist[list_start:list_end]])
