from numpy import pi


class A():
    def __init__(self):
        pass

    def __call__(self, f):
        def wrap(*args, **kwargs):
            print('Starting decorating {}'.format(f.__name__))
            res = f(*args, **kwargs)
            print(res)
            print('Done decorating {}'.format(f.__name__))

        return wrap


def area_square(a=1, b=1):
    return a * b


deco_instance = A()


@deco_instance
def area_circle(r):
    return (r ** 2) * pi


area_circle(5)  # Calling the decorated version

# This is what is happening in the background when we decorate a function with instance
# decorator this returns an object of the class which is callable and then we are calling it

area_square = A()(area_square)
area_square(5, 10)  # calling the callable instance also returns a callable

# Using the syntactic sugar for instance decorator
