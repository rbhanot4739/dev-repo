def calc(func, a, b):
    print("The name of the function passed as parameter to this function is ", func.__name__)
    return func(a, b)


def add(x, y):
    print(x + y)


def mul(x, y):
    print(x * y)


calc(add, 5, 8)
calc(mul, 5, 8)
