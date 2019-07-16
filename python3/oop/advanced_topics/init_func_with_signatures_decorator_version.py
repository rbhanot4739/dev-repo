import sys
from inspect import Signature, signature, Parameter
from functools import partial


class Init:
    _attrs = []

    def __init__(self, *args):
        if len(args) != len(self._attrs):
            sys.exit("Invalid no of args passed")
        for i, j in zip(self.__class__._attrs, args):
            setattr(self, i, j)


class Person(Init):
    _attrs = ['name', 'age']


class Planet():
    _attrs = ['weight', 'radius', 'name']


# e = Planet(89, 98989, 'earth')
# e = Planet(89, 98989, name='earth')

# The problem with above approach is that it does not handle keyword args
# and it also looses the function signatures
# To fix this we need to built custom signatures


def make_signature(names):
    args = [Parameter(name, Parameter.POSITIONAL_OR_KEYWORD) for name in names]
    signature_object = Signature(args)
    return signature_object

#
# names = ('a', 'b', 'c')
# params = make_signatures(names).bind(1, 2, 3)
#
#
# # print(params.arguments)


def add_signatures(fields=None, cls=None):
    if cls is None:
        return partial(add_signatures, fields)
    cls.__signature__ = make_signature(fields)
    return cls


@add_signatures(fields=[])
class Base(object):
    # _attrs = []
    # __signature__ = make_signature(_attrs)

    def __init__(self, *args, **kwargs):
        params = self.__signature__.bind(*args, **kwargs)
        for name, val in params.arguments.items():
            setattr(self, name, val)


@add_signatures(['a', 'b'])
class A(Base):
    pass
    # _attrs = ['a', 'b']
    # __signature__ = make_signature(_attrs)


@add_signatures(fields=['x', 'y', 'z', 'q'])
class B(Base):
    pass
    # _attrs = ['x', 'y', 'z', 'q']
    # __signature__ = make_signature(_attrs)


a = A(1, 2)
b = B(10, 20, z='hello', q='world')


print(signature(A))
print(signature(B))
