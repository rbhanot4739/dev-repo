def simple_decorator(func):
    func.msg = 'This is a test message attached to function'
    return func


@simple_decorator
def add(*args):
    return sum(args)


@simple_decorator
def maxi(*args):
    return max(args)


def newmethod360():
    return add


# print(newmethod360().msg)
# print(newmethod360()(2, 4, 5, 6))
# print(maxi.msg)
print(maxi(2, 4, 9, 5, 6))
