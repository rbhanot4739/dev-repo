class Descriptor:
    def __get__(self, instance, owner):
        if instance is None:
            return self
        else:
            return instance.__dict__[self.attr_name]


class Positive(Descriptor):

    # Instead of creating a weakDict of with each instance as key in the
    # descriptor class, you can save the attributes directly inside the
    # __dict__ of instance but this requires the descriptor class to know
    # the attribute name in advance AND THIS IS NOT AS EASY AS IT SOUNDS

    # This class uses a work around to store the attribute names
    # which are passed inside the owner class when Descriptor object is
    # instantiated. But this is not reliable or very practical

    def __init__(self, attr_name):
        self.attr_name = attr_name  # self.attr_name = '_' + attr_name

    # def __get__(self, instance, owner):
    #     # return getattr(instance, self.attr_name)
    #     return instance.__dict__[self.attr_name]

    def __set__(self, instance, value):
        if value < 1:
            instance.__dict__[self.attr_name] = 1
        else:
            instance.__dict__[self.attr_name] = value


class Rectangle:
    length = Positive("length")
    breadth = Positive("breadth")

    def __init__(self, len_val, bre_val):
        self.length = len_val
        self.breadth = bre_val

    @property
    def area(self):
        return self.length * self.breadth


r1 = Rectangle(10, 20)
print('***** Rectangle Obj1 created *****')
print('r1(Length = {}, breadth = {}, area = {})'.format(r1.length, r1.breadth,
                                                        r1.area))
r2 = Rectangle(100, 200)
print('***** Rectangle Obj2 created *****')
print('r2(Length = {}, breadth = {}, area = {})'.format(r2.length, r2.breadth,
                                                        r2.area))
print('r1(Length = {}, breadth = {}, area = {})'.format(r1.length, r1.breadth,
                                                        r1.area))


class Uppercase(Descriptor):

    def __set__(self, instance, value):
        if isinstance(value, str):
            instance.__dict__[self.attr_name] = value.upper()
        else:
            raise TypeError("{}.{} need to be a"
                            " string".format(instance.__class__.__name__,
                                             self.attr_name))


def decorate_descriptor(cls):
    for key, val in cls.__dict__.items():
        # hasattr(val, '__dict__') this is gonna be true only for descriptor
        #  attributes, b'coz they are instances of descriptor class
        if isinstance(val, Descriptor):
            val.attr_name = key
    return cls


# The below class does not pass the attributes names instead uses the decorator


@decorate_descriptor
class Book:
    title = Uppercase()
    author = Uppercase()
    price = 200

    def __init__(self, book_title, book_author):
        self.title = book_title
        self.author = book_author

    def __repr__(self):
        return "{}({!r}, {!r}, {!r})".format(self.__class__.__name__,
                                             self.title, self.author,
                                             self.price)


b1 = Book('fluent python', 'luciano ramalho')
b2 = Book('python cookbook', 'david beazly')
print(b1)
print(b2)
