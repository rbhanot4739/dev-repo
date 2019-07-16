import multiprocessing, os
from time import sleep
from sys import platform
from threading import Thread


def greet(num=None):
    cp = multiprocessing.current_process()
    print('Greeting message from {} with PID = {}'.format(cp.name, cp.pid))
    for i in range(num):
        _ = i ** 4
    # sleep(10)


if __name__ == "__main__":
    print('Pid of Main Process is {}'.format(os.getpid()))
    procs = []
    for i in range(5):
        if platform == 'linux':
            # p = multiprocessing.Process(target=greet, args=(100000000,))
            p = Thread(target=greet, args=(100000,))
            procs.append(p)
            p.start()
    # sleep(20)
    for proc in procs:
        proc.join()
