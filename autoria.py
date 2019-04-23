from time import time
from autoria_sub import *
from database import create_bd
from helpers import timer
from constants import RIA_THREAD_COUNT

start = time()

create_bd()
get_links()

if RIA_THREAD_COUNT == 0:
    GetData(queue_in, queue_out).run()
    StoreData(queue_out).run()
else:
    # Create threads for parsing links
    for _ in range(RIA_THREAD_COUNT):
        t = GetData(queue_in, queue_out)
        t.daemon = True
        t.start()

    # Create a thread for data storing to db
    db_thread = StoreData(queue_out)
    db_thread.daemon = True
    db_thread.name = 'Thread-DB'
    db_thread.start()

    queue_in.join()
    queue_out.join()

# Measure time spent
logger.info("Time spent: " + timer(start, time()))
