count = 1000000

from collections import namedtuple
import sys

myTuple = namedtuple("Ints", ['a', 'b', 'c', 'd'])
n = []


class normal(object):
    # __slots__ = ['a', 'b', 'c', 'd']
    def __init__(self, a, b, c, d):
        self.a = a
        self.b = b
        self.c = c
        self.d = d


# for i in range(count):
#    n.append(myTuple(i+1, i+2, i+3, i+4))
#
for i in range(count):
    n.append((i + 1, i + 2, i + 3, i + 4))

# for i in range(count):
#    n.append(normal(i+1, i*2, i**3, 4*i))
