from weakref import WeakKeyDictionary


class Positive:
    """
     ===== Problem with this descriptor=====
    Because we are storing the value in descriptor instance, this will
    cause all instances of the owner class to share the value. To test
    create multiple objects of the owner class and then see if value in
    object affects other.
    You can also inspect __dict__ of Positive's instance in owner
    class through manual debugging

    To solve this we need to store the attribute values of an instance
    in its own separate dictionary inside the descriptor
    """
    def __get__(self, instance, owner):
        return self.value

    def __set__(self, instance, value):
        if value < 1:
            raise Exception("Negative or zero is not allowed")
        else:
            self.value = value


class Rectangle:
    length = Positive()
    breadth = Positive()

    def __init__(self, len_val, bre_val):
        self.length = len_val
        self.breadth = bre_val


r1 = Rectangle(10, 20)
print('***** Rectangle Obj1 created *****')
print('r1(Length = {}, breadth = {})'.format(r1.length, r1.breadth))
r2 = Rectangle(100, 200)
print('***** Rectangle Obj2 created *****')
print('r2(Length = {}, breadth = {})'.format(r2.length, r2.breadth))
print('r1(Length = {}, breadth = {})'.format(r1.length, r1.breadth))


class NonNegative:
    """
    While this version improves on the previous one by using a weak key dict, but this 
    also one major drawback which is that we are storing the values in the descriptor not
    on the actual owner class instance where it actually belongs    
    
    """

    def __init__(self):
        # we are using a weakkey dictionary here rather than a regular dict because weakkey dict will be
        # automatically garbage collected once all the keys in it are deleted and keys in this dict will be instances
        # of the class where descriptor is initialized and once the instances go out of scope, this weak key dict will also
        # out of scope, this won't happen for a regualr dict.
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

    def __init__(self, value1, value2):
        self.length = value1
        self.breadth = value2


c1 = Cube(20, 10)
print('\n***** Cube Obj1 created *****')
print('c1(Length = {}, breadth = {})'.format(c1.length, c1.breadth))
c2 = Cube(30, 40)
print('***** Cube Obj2 created *****')
print('c2(Length = {}, breadth = {})'.format(c2.length, c2.breadth))
print('c1(Length = {}, breadth = {})'.format(c1.length, c1.breadth))
