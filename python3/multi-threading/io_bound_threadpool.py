import threading
from time import time
from queue import Queue
import requests




def get_url(queue):
    while not queue.empty():
        url = queue.get()
        resp = requests.get(url)
        print(url, ' ', len(resp.text), ' bytes', 'Being handled by', threading.current_thread().getName())
        queue.task_done()

urls = ('http://www.google.com', 'http://www.yahoo.com', 'http://www.msn.com', 'http://www.aol.com',
        'http://www.wikipedia.com', 'http://www.espncricinfo.com', 'http://www.discovery.com',
        'http://www.timesofindia.com', 'http://www.cricbuzz.com')
t1 = time()
q = Queue()

for item in urls:
    q.put(item)

# get_url(q)

threads = []
for _ in range(5):
    th = threading.Thread(target=get_url, args=(q,))
    threads.append(th)
    th.start()

q.join()
print('Time taken = ', time() - t1)


