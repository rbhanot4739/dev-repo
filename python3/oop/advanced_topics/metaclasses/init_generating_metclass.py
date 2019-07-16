from inspect import signature


def _make_init(fields):
    code = "def __init__(self, {}):\n".format(','.join(fields))
    for field in fields:
        code += '    self.{} = {}\n'.format(field, field)
    return code


class MyMeta(type):
    def __new__(mcs, clsname, bases, clsdct):
        if clsdct['_attrs']:
            exec(_make_init(clsdct['_attrs']), globals(), clsdct)
        return super().__new__(mcs, clsname, bases, clsdct)


class Base(metaclass=MyMeta):
    _attrs = []


class A(Base):
    _attrs = ['a', 'b']


class B(Base):
    _attrs = ['x', 'y', 'z', 'q']


a = A(1, 2)
b = B(10, 20, z='hello', q='world')

print(signature(B))
print(signature(A))
