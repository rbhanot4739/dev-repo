from functools import reduce
from operator import add, mul


def double(x):
    return x * 2


def div(x):
    if x % 2 == 0:
        return x


# quick way to create lists for ranges
nums = list(range(-10, 10))
nums2 = list(range(30, 40))
words = ['hello', 'world', 'this', 'is', 'python', 'code']

print(nums)
print(words)
# lambda implementation

f = lambda i, j: i ** 2 + j
print(f)
print(f(3, 4))

# Map implementations
print('\n', '*' * 30, 'Map', '*' * 30, '\n')
print(list(map(double, nums)))  # Mapping fxn s to list nums
print(list(map(lambda i: i ** 2, nums)))  # mapping a lambda fxn for sqaring to list nums
print(list(map(len, words)))  # Mapping builtin len fxn of python to find length of strings

# Map can take multiple iterable as well as its args

print(list(map(mul, nums, nums2)))

# Filter implementation

print('\n', '*' * 30, 'Filter', '*' * 30, '\n')
# If None is passed as 1st arg to Filter then it filters only True values

print(list(filter(None, ('', 23, 0, 'Helo', [1, 2, 3], [], (), (11, 21), {}, {'a': 'b'}))))
print(list(filter(lambda x: x > 0, nums)))
print(list(filter(div, nums)))

# Reduce implementation

print('\n', '*' * 30, 'Reduce', '*' * 30, '\n')
print(reduce(lambda x, y: x + y, nums))
print(reduce(max, nums))
print(reduce(min, nums))

print('\n', '*' * 60, '\n')
print("Combining Map Filter & Reduce to find out Sum of cubes of positive & negative numbers ")

print(reduce(lambda x, y: x + y, list(map(lambda x: x ** 3, list(filter(lambda x: x > 0, nums))))))
print(reduce(lambda x, y: x + y, list(map(lambda x: x ** 3, list(filter(lambda x: x < 0, nums))))))
