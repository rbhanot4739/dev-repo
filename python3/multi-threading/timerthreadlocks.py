import threading
from time import sleep

lock = threading.Lock()


def threader(reps):
    with lock:
        print('{} started'.format(threading.current_thread().name))
        print('{} finished'.format(threading.current_thread().getName()))


if __name__ == "__main__":
    timers = []
    for i in range(3):
        t = threading.Thread(target=threader, args=(3,))
        timers.append(t)
        t.start()

    for t in timers:
        t.join()
