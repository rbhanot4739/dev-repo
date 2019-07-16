import threading
import time
import signal


def non_daemon():
    # print('Starting {} with a sleep of 0.5 secs'.format(
    #     threading.current_thread().name))
    for _ in range(10):
        time.sleep(0.5)
        print(_)


def daemon():
    # print('Starting {} with a sleep of 5 secs'.format(threading.current_thread().name))
    for _ in range(1000):
        time.sleep(0.5)
        # print('isDaemon -> {}'.format(threading.current_thread().isDaemon()))
        print(_)

if __name__ == "__main__":
    try:
        # threads = [threading.Thread(name='non_daemon', target=non_daemon)
        #            for _ in range(8)]
        # for th in threads:
        #     th.start()

        d_threads = [threading.Thread(name='daemon', target=daemon)
                   for _ in range(8)]

        for th in d_threads:
            th.daemon = True
            th.start()


        for th in d_threads:
            while th.isAlive():
                th.join(1)

        # while True:
        #     time.sleep(1)
        # # signal.pause()

    except KeyboardInterrupt:
        print('ctrl-c')
