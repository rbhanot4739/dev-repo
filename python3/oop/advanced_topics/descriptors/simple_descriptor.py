from weakref import WeakKeyDictionary


class Positive:

    # Problem 1
    # Because we are storing the value in descriptor instance, this will
    # cause all instances of the owner class to share the value. To test
    # create multiple objects of the owner class and then see if value in
    # object affects other.
    # You can also inspect __dict__ of Positive's instance in owner
    # class through manual debugging

    # To solve this we need to store the attribute values of an instance
    # in its own separate dictionary inside the descriptor

    def __get__(self, instance, owner):
        return self.value

    def __set__(self, instance, value):
        if value < 1:
            raise Exception("Negative or zero is not allowed")
        else:
            self.value = value


class Rectangle:
    # Descriptors objects are created at class level to make sure that __set__
    # executed on class's object initialization as well.
    length = Positive()
    breadth = Positive()

    def __init__(self, len_val, bre_val):
        self.length = len_val
        self.breadth = bre_val

    @property
    def area(self):
        return self.length * self.breadth


r1 = Rectangle(10, 20)
print('***** Rectangle Obj2 created *****')
print('r1(Length = {}, breadth = {}, area = {})'.format(r1.length, r1.breadth,
                                                        r1.area))
r2 = Rectangle(100, 200)
print('***** Rectangle Obj2 created *****')
print('r2(Length = {}, breadth = {}, area = {})'.format(r2.length, r2.breadth,
                                                        r2.area))
print('r1(Length = {}, breadth = {}, area = {})'.format(r1.length, r1.breadth,
                                                        r1.area))


class NonNegative:

    def __init__(self):
        self.instances = WeakKeyDictionary()

    def __get__(self, instance, owner):
        # print('getting the value')
        return self.instances.get(instance, 'None')

    def __set__(self, instance, value):
        if value > 0:
            # print('setting the value for ', instance)
            self.instances[instance] = value
        else:
            raise Exception("Negative or zero is not allowed")


class Cube(object):
    length = NonNegative()
    breadth = NonNegative()
    height = NonNegative()

    def __init__(self, value1, value2, value3):
        self.length = value1
        self.breadth = value2
        self.height = value3


c1 = Cube(20, 10, 50)
print('\n***** Cube Obj1 created *****')
print(
    'c1(Length = {}, breadth = {}, height = {})'.format(c1.length, c1.breadth,
                                                        c1.height))
c2 = Cube(30, 40, 80)
print('***** Cube Obj2 created *****')
print(
    'c2(Length = {}, breadth = {}, height = {})'.format(c2.length, c2.breadth,
                                                        c2.height))
print(
    'c1(Length = {}, breadth = {}, height = {})'.format(c1.length, c1.breadth,
                                                        c1.height))
