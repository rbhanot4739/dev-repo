import multiprocessing
import random
import os
from threading import Thread


def square(val, nums=None, result=None):
    for num in nums:
        result.append(num ** 2)

    print('Result = {} in new created {} "{}"'.format(result, val, os.getpid()))


nums = random.sample(range(1, 30), 5)

if __name__ == "__main__":
    print('\n*****  PID of Main Process is {} *****\n'.format(os.getpid()))
    result = []
    print('Result={} before starting a new Process with Multiprocessing module'.format(result))
    p1 = multiprocessing.Process(target=square, args=('Process', nums, result,))
    p1.start()
    p1.join()
    print('Result = {} after the new process has ended'.format(result))
    print('\nResult = {} before creating a new Thread with Threading module'.format(result))
    t1 = Thread(target=square, args=('Thread', nums, result,))
    t1.start()
    t1.join()
    print('Result = {} after the new Thread has exited'.format(result))
