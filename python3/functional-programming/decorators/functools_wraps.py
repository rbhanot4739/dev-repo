import functools


def dec1(f):
    def wrap():
        """ The wrapper function for the decorator """
        f()

    return wrap


def dec2(f):
    @functools.wraps(f)
    def wrap():
        """ The wrapper function for the decorator """
        print('Decorating !!')
        f()

    return wrap


@dec1
def hello():
    """ Prints a hello message"""
    pass


@dec2
def bye():
    """ Prints a bye message """
    pass


hello()
print(
    'Printing __name__ and __doc__ of decorated function "{}" whose wrapper isn\'t decorated with functools.wraps()'.format(
        hello))
print('__name__ : {}, __doc__: {}\n'.format(hello.__name__, hello.__doc__))
print('-' * 50)
bye()
print(
    'Printing __name__ and __doc__ of decorated function"{}" whose wrapper is decorated with functools.wraps()'.format(
        bye))
print('__name__ : {}, __doc__: {}'.format(bye.__name__, bye.__doc__))
