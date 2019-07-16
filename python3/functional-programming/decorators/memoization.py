import time
from functools import lru_cache, wraps
from recursive_decorator import show_time
from count_fxn_calls import func_counter


#################################################################
# Builtin Memoization with Functools
#################################################################

# @lru_cache()
# def fib(n):
#     if n == 0:
#         return 0
#     elif n == 1:
#         return 1
#     else:
#         return fib(n-1) + fib(n-2)

#################################################################
# Memoization - Manual
#################################################################

cache ={}
def fib(n):
    if n in cache:
        return cache[n]
    # elif n == 0:
    #         cache[n]=0
    #         return cache[n]
    elif n < 2:
        cache[n] = 1
        return cache[n]
    else:
        cache[n]= fib(n-1) + fib(n-2)
        return cache[n]

#################################################################
# Memoization - With decorators
#################################################################

# def memoize(func):
#     cache = {}
#
#     @wraps(func)
#     def wrapper(j):
#         if j not in cache:
#             cache[j] = func(j)
#         return cache[j]
#
#     return wrapper
#
#
# @func_counter
# # # @show_time
# @memoize
# def fib(n):
#     if n == 0:
#         return 0
#     elif n == 1:
#         return 1
#     else:
#         return fib(n - 1) + fib(n - 2)
#
#
################################################################


if __name__ == "__main__":
    # for i in range(10):
    #     print(fib(i))
    print(fib(8))
# print("Number of calls for fib {}". format(fib.count))
