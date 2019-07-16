import sys


class A():
    def __init__(self, x, y):
        self.x = x
        self.y = y


class B():
    def __init__(self, p, q):
        self.p = p
        self.q = q

# The above is a typical method of creating classes with every class having
# its own init method. Below is different way to solve this


class Init():
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


e = Planet(89, 98989, 'earth')
