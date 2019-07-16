import sys


# Attribute lookup order
# 1. Lookup is made in Data Descriptor if exists
# 2. __dict__ of object is searched
# 3. Non-Data descriptor is looked for attribute


class DataDescriptor(object):
    def __init__(self, attribute):
        self.default = 100
        self.attribute = attribute

    def __get__(self, instance, owner):
        print('Getting the value of', self.attribute,
              '__get__ of Data descriptor invoked')
        return instance.__dict__.get(self.attribute, self.default)

    def __set__(self, instance, value=200):
        if value > 0:
            print('__set__ of Data descriptor invoked')
            instance.__dict__[self.attribute] = value
        else:
            sys.exit('Negative value not allowed')


class NonDataDescriptor(object):
    def __init__(self, attribute):
        self.default = 10
        self.attribute = attribute

    def __get__(self, instance, owner):
        print('Getting the value of', self.attribute,
              '__get__ of Non-Data descriptor invoked')
        instance.__dict__[self.attribute] = self.default
        return instance.__dict__.get(self.attribute, self.default)


class Rectangle(object):
    length = DataDescriptor("length")
    breadth = NonDataDescriptor("breadth")


obj = Rectangle()
print(obj.length)
print(obj.breadth)

print(obj.length)
print(obj.breadth)
