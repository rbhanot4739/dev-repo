from itertools import chain
from timeit import timeit
import collections

l = [[1, 2, 3], [4, 5], [6], [7, 8, 9, 10]] * 999


#
# # Method 1 using list comprehension
#
# print('Using list comprehensions')
# # l1 = [elem for subl in l for elem in subl]
# print('Time taken {:.9f}'.format(
#     timeit(setup='from __main__ import l', stmt='[elem for subl in l for elem in subl]', number=10)))
#
# print('Using Sum function')
# l2 = sum(l, [])
# print(l2)
# print('Time taken {:.9f}'.format(
#     timeit(setup='from __main__ import l', stmt='sum(l, [])', number=10)))
#
# print('Using Itertools.chain.from_iteratable')
# # l3 = chain.from_iterable(l)
# print(
#     'Time taken {:.9f}'.format(timeit(setup='from __main__ import l, chain', stmt='chain.from_iterable(l)', number=10)))


def flattener(li):
    for item in li:
        if isinstance(item, collections.Iterable):
            flattener(item)
        else:
            l2.append(item)
    return l2


#
#
l2 = []
l1 = [1, 2, 78, [3, 4], [5, [6, 7, (11, [12, 33, (9788, 78, [35, 909])], 22)]], 8]


# print(flattener(l1))


def flattner_generator(li):
    for item in li:
        if isinstance(item, collections.Iterable):
            yield from flattner_generator(item)
        else:
            yield item


for gen in flattner_generator(l1):
    print(gen, end=', ')
