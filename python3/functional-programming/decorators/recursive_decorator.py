import time
from functools import wraps
from count_fxn_calls import func_counter


def show_time(f):

    wraps(f)

    def wrapper(*args):
        # print('Decorating', args)
        t1 = time.time()
        res = f(*args)
        # print(res, '----')
        t2 = time.time() - t1
        print('[{:.8f}] -> {}({}) = {}'.format(t2, f.__name__, ''.join(
            str(i) for i in args),  res))
        return res

    return wrapper


# @func_counter
@show_time
# fact = deco_fact(fact)
def fact(n):
    # res = 1
    # for i in range(n, 0, -1):
    #     res = res * i
    # return res
    if n == 0:
        return 1
    else:
        return n * fact(n - 1)


if __name__ == '__main__':
    print(fact(19))
    # print(fact.count)
