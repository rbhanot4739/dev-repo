from threading import Thread
import os


def greet():
    print('Doing some stuff')
    print('Total number of CPU Cores on this system = {}'.format(os.cpu_count()))
    print('No of CPU Cores that can be used by this Thread = {}'.format(len(os.sched_getaffinity(0))))


t1 = Thread(target=greet)
t1.start()
t1.join()
