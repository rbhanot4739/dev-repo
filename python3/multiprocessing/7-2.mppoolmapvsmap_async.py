# Pool.map blocks until result is calculacted and returned
# Pool.map_async doesn't block and returns to main however the get() is blocked.

import multiprocessing as mp
import time


def f(x):
    time.sleep(1)
    print('sleeping in child')
    return x * x


if __name__ == '__main__':
    po = mp.Pool(processes=4)

    print('Before pool')
    # res = po.map(f, range(3))
    # print(res)

    res = po.map_async(f, range(3))

    # #	You can start the Pool and then carry on with stuff in main process and at later stage you can get the results.

    # print(res.get())

    print('After pool')
    po.close()
    po.join()
