from multiprocessing import Process, Queue
from time import sleep


def fun1(q):
    data = [1, 2, 3, 'Hello World']
    q.put(data)
    q.put('Text from Func1')
    sleep(3)
    q.put('Fun1 done')


def fun2(q):
    data = (10, 20, 30)
    q.put(data)
    q.put('Text from Func2')
    q.put('Finish')


if __name__ == '__main__':
    q = Queue()
    p1 = Process(target=fun1, args=(q,))
    p2 = Process(target=fun2, args=(q,))
    p1.start()
    p2.start()

    while True:
        msg = q.get()

        if msg == 'Finish':
            print('Exiting from the queue')
            break
        print(msg)

    p1.join()
    p2.join()
