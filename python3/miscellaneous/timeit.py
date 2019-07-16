# Simple Timeit example

# t=timeit.Timer('print("Test")','print("Setup")')
# print(t.timeit(5))
# print(t.repeat(3,5))

def fib(n):
    if n is 0:
        return 0
    elif n is 1:
        return 1
    else:
        return fib(n - 1) + fib(n - 2)


def memoized_fib(n):
    if n in cache:
        return cache[n]
    elif n is 1:
        cache[n] = 1
    elif n is 0:
        cache[n] = 0
    else:
        cache[n] = memoized_fib(n - 1) + memoized_fib(n - 2)
    return cache[n]


if __name__ == "__main__":
    import timeit

    cache = {}
    t1 = timeit.timeit('fib(40)', 'from __main__ import fib', number=1)
    t2 = timeit.timeit('memoized_fib(40)', 'from __main__ import memoized_fib', number=1)
    print("Normal recursive Fibonacci for 30 numbers took {} secs ".format(t1))
    print("Memoized recursive Fibonacci for 30 numbers took {} secs ".format(t2))
