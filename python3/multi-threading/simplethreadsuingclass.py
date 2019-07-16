import random
import threading
import time


class SleepingThread(threading.Thread):
    sleep_length = None

    def __init__(self, sleep_length=None):
        super().__init__()
        self.sleep_length = sleep_length or random.randrange(1, 5)

    def run(self):
        print(threading.current_thread().getName(), "starting")
        time.sleep(self.sleep_length)


if __name__ == '__main__':
    # create and start our threads
    threads = []
    for i in range(4):
        t = SleepingThread()
        threads.append(t)
        t.start()

    # wait for each to finish (join)
    for t in threads:
        t.join()
