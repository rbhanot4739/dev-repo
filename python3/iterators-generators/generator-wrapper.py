def OddNumbers(upper):
    num = 1
    while num < upper:
        if num % 2 != 0:
            yield num
        num += 1


# class OddNumbers(object):
#     def __init__(self, upper):
#         self.upper = upper
#
#     def __iter__(self):
#         self.num = 1
#         while self.num < self.upper:
#             if self.num %2 == 0:
#                 yield self.num
#             self.num += 1


def powers(nums, n):
    squares = map(lambda x: x ** 2, nums(n))
    cubes = map(lambda x: x ** 3, nums(n))

    for i in squares:
        print(i)
    print('-------')
    for i in cubes:
        print(i)


def wrapper(n):
    # yield from OddNumbers(n)
    obj = OddNumbers(n)
    return obj


# nums = OddNumbers(10)
powers(wrapper, 20)
