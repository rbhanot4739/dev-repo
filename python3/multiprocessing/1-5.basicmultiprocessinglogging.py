import multiprocessing
import logging, os


def greet():
    print('Doing some work')
    print('Total number of CPU Cores on this system = {}'.format(os.cpu_count()))
    print('No of CPU Cores that can be used by this Process = {}'.format(len(os.sched_getaffinity(0))))


if __name__ == '__main__':
    multiprocessing.log_to_stderr(logging.INFO)
    p1 = multiprocessing.Process(target=greet)
    p1.start()
