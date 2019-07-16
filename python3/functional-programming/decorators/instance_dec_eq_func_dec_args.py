def dec(val):
    def real_dec(f):
        def wrapper(*args, **kwargs):
            if val:
                print('Decorating the function "{}" with Parametrized Decorator'.format(f.__name__))
            return f(*args)

        return wrapper

    return real_dec


@dec(True)
def greet():
    return 'Hello !!!'


@dec(False)
def bye():
    return 'bye'


print(greet())
print('-' * 30)
print(bye())


class Dec():
    def __init__(self, val):
        self._val = val

    def __call__(self, f, *args, **kwargs):
        def wrap(*args):
            if self._val:
                print('Decorating the function "{}" with Instance Decorator'.format(f.__name__))
            return f(*args)

        return wrap


@Dec(True)
def hello():
    return 'Hello'


@Dec(False)
def hie():
    return 'Hie'


print(hello())
print('*' * 30)
print(hie())
