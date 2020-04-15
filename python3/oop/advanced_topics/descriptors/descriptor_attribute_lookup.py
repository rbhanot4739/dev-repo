# Attribute lookup order
# 1. Lookup is made in Data Descriptor if exists
# 2. __dict__ of object is searched
# 3. Non-Data descriptor is looked for attribute
# 4. if it is not a valid attribute __getattr__ is invoked


class DataDescriptor(object):
    def __init__(self, attribute):
        self.default = 100
        self.attribute = attribute

    def __get__(self, instance, owner):
        print('Getting the value of', self.attribute,
              '> __get__ of Data descriptor invoked > val = ', end='')
        return instance.__dict__.get(self.attribute, self.default)

    def __set__(self, instance, value=200):
        if value > 0:
            print('__set__ of Data descriptor invoked')
            instance.__dict__[self.attribute] = value
        else:
            raise ValueError('Negative value not allowed')


class NonDataDescriptor(object):
    def __init__(self, attribute):
        self.default = 10
        self.attribute = attribute

    def __get__(self, instance, owner):
        print('Getting the value of', self.attribute,
              '> __get__ of Non-Data descriptor invoked > val = ', end='')
        return instance.__dict__.get(self.attribute, self.default)


class Rectangle(object):
    length = DataDescriptor("length")
    breadth = NonDataDescriptor("breadth")

    def __init__(self, x, y):
        self.length = x
        self.height = y

    def __getattr__(self, item):
        return f"{self}.{item} does not exist ==> __getattr__ invoked"

obj = Rectangle(22, 33)
print(obj.breadth)
print(obj.length)
print(obj.height)
obj.__dict__['breadth'] = 300
print("fetched from obj.__dict__", obj.breadth, "")
print(obj.fake_attr)
print(obj.__dict__)
