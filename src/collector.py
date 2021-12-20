import os
import time
from api.batcher_api import post_pop_batch

host = os.environ["BATCHER_HOST"]


def job():
    try:
        batch = post_pop_batch(host)
        print(batch)
    except ConnectionError:
        print("Exited with network error")
        exit(1)


if __name__ == "__main__":
    while True:
        job()
        time.sleep(2)
