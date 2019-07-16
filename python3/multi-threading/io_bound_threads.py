from threading import Thread
import time
import os


def dir_lister(path):
    for i in os.walk(path):
        for file in i[-1]:
            try:
                os.path.join(i[0], file)
            except Exception as e:
                continue


# Sequential execution

t1 = time.time()
for _ in range(40):
    dir_lister("/apps/nttech/rbhanot/Documents/")

# dir_lister("/spare/local/repos/")

t2 = time.time()
st = t2 - t1
print('Sequential execution took {:.2f} seconds'.format(t2 - t1))

# # Threaded execution

t3 = time.time()
threads = []
for _ in range(40):
    th = Thread(target=dir_lister, args=("/apps/nttech/rbhanot/Documents/",))
    threads.append(th)
    th.start()

for thread in threads:
    thread.join()

t4 = time.time()
tt = t4 - t3
print('Concurrent execution took {:.2f} seconds'.format(t4 - t3))

print('Threaded execution for IO bound task was {:,.1f} times faster'.format(st / tt))
