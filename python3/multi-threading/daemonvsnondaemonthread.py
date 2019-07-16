import threading
import time


def nondaemon():
    print('Starting {} with a sleep of 0.5 secs'.format(
        threading.current_thread().name))
    for _ in range(100):
        time.sleep(0.5)
        print('Non-Daemon')


def daemon():
    print('Starting {} with a sleep of 5 secs'.format(threading.current_thread().name))
    for _ in range(100):
        time.sleep(0.5)
        print('Non-Daemon')


if __name__ == "__main__":
    try:
        # t = threading.Thread(name='Non-daemon', target=nondaemon)
        # t.start()
        # t.join()
        # print("t.isAlive() {}".format(t.isAlive()))
        d = threading.Thread(name='Daemon', target=daemon, daemon=True)
        d.start()
        d.join() # it will block
        print("d.isAlive() {}".format(d.isAlive()))
    except KeyboardInterrupt:
        print('ctrlc')
