from inspect import Signature, signature, Parameter


# The solves the func signature prob with metaclass


def make_signature(names):
    args = [Parameter(name, Parameter.POSITIONAL_OR_KEYWORD) for name in names]
    signature_object = Signature(args)
    return signature_object


class SignatureMeta(type):

    def __new__(mcs, clsname, bases, clsdict):
        clsdict['__signature__'] = make_signature(clsdict['_attrs'])
        return super().__new__(mcs, clsname, bases, clsdict)


class Base(metaclass=SignatureMeta):
    _attrs = []

    def __init__(self, *args, **kwargs):
        params = self.__class__.__signature__.bind(*args, **kwargs)
        for name, val in params.arguments.items():
            setattr(self, name, val)


class A(Base):
    _attrs = ['a', 'b']


class B(Base):
    _attrs = ['x', 'y', 'z', 'q']


a = A(1, 2)
b = B(10, 20, z='hello', q='world')

print(signature(B))
print(signature(A))

# b = Base()
# print(Base.__dict__)
