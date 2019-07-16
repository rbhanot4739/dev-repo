from functools import partial, wraps


def debug(func=None, prefix=''):
    if func is None:
        # print('partial')
        return partial(debug, prefix=prefix)

    msg = prefix + func.__qualname__ + prefix

    @wraps(func)
    def wrapper(*args, **kwargs):
        print(msg)
        return func(*args, **kwargs)

    return wrapper


def debugClass(cls):
    for k, v in vars(cls).items():
        if callable(v):
            setattr(cls, k, debug(v))
    return cls


@debug(prefix='--')
# the above statment translates --> test = debug(prefix)(test)
def test():
    print("Hello")


@debugClass
class A:
    def one(self):
        pass

    def two(self):
        pass

    # class/static methods arn't affected when you decorate the entire class
    # Wny ? To find out inspect __dict__ of class and see are class/static
    # methods really or are they callable objects !!
    @staticmethod
    def three():
        pass


test()
# pdb.set_trace()

a = A()
a.one()
a.two()
a.three()
