class MyMeta(type):

    def __new__(mcs, cls, bases, dct):
        for k, v in dct.items():
            if isinstance(v, Descriptor):
                dct[k].attr_name = k
        return super().__new__(mcs, cls, bases, dct)


class Descriptor:
    def __get__(self, instance, owner):
        if instance is None:
            return self
        else:
            return instance.__dict__[self.attr_name]


class Positive(Descriptor):

    def __set__(self, instance, value):
        if value < 1:
            raise Exception(
                "{}.{} can't be negative".format(instance.__class__.__name__,
                    self.attr_name))
        else:
            instance.__dict__[self.attr_name] = value


class Rectangle(metaclass=MyMeta):
    length = Positive()
    breadth = Positive()

    def __init__(self, length, breadth):
        self.length = length
        self.breadth = breadth

    def __repr__(self):
        return "{}({!r}, {!r})".format(self.__class__.__name__, self.length,
                                       self.breadth)


r1 = Rectangle(4, 20)
r2 = Rectangle(100, 200)
r3 = Rectangle(400, 124)
r4 = Rectangle(123, 245)
# print(r1, r2)
# r1.breadth = 30
# r2.length = 150
# print(r1, r2)
