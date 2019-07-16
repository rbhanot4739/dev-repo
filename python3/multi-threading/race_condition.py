import threading
from time import sleep
from random import random

count = 0


def counter():
    sleep(random())
    global count
    sleep(random())
    count += 1
    sleep(random())
    print('----- {} --> count = {} -----'.format(threading.current_thread().getName(), count))
    sleep(random())


print('----- Starting -----')
threads = []

for _ in range(10):
    th = threading.Thread(target=counter)
    threads.append(th)
    th.start()

for th in threads:
    th.join()

print('----- Finishing -----')
