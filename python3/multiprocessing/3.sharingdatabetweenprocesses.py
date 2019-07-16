# Using MP Array and Value to share data b/w main process and child process.

import multiprocessing, random, os
from threading import Thread


def pows(nums=None, sqrs=None, cubs=None):
    for id, num in enumerate(nums):
        sqrs.append(num ** 2)
        cubs[id] = num ** 3


if __name__ == "__main__":
    nums = random.sample(range(1, 30), 5)
    print(' \n************   PID of Main Process is {}  ************\n'.format(os.getpid()))

    squares = []
    cubes = multiprocessing.Array('i', 5)
    value = multiprocessing.Value('i', 5)
    print('------- Before starting a new Process with Multiprocessing module -------\nSquares = {}\nCubes = {}'.format(
        squares, cubes[:]))
    p1 = multiprocessing.Process(target=pows, args=(nums, squares, cubes))
    p1.start()
    p1.join()
    print('------- After starting a new Process with Multiprocessing module -------\nSquares = {}\nCubes = {}'.format(
        squares, cubes[:]))
