# Case 1: Executing independent tasks / Same task multiple times
# This will not benefit from multi core system as GIL will only let one thread run at a time

from threading import Thread, current_thread
import time


def counter(n):
    sqr = 0
    print('Starting', current_thread().name)
    while n > 0:
        sqr += n**2
        n -= 1
    print('Stopping', current_thread().name)
    print(sqr)


# Sequential execution
t1 = time.time()
count = 900000

# counter(count)

t2 = time.time()
print('Sequential execution took {:.2f} seconds'.format(t2 - t1))

# Threaded execution
t3 = time.time()
threads = []
for _ in range(5):
    th = Thread(target=counter, args=(count,))
    threads.append(th)
    th.start()

for thread in threads:
    thread.join()

t4 = time.time()
print('Parallel execution took {:.2f} seconds'.format(t4 - t3))
