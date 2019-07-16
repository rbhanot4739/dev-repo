# https://realpython.com/blog/python/instance-class-and-static-methods-demystified/


class TestClass:
    def __init__(self, fname, lname):
        self.fname = fname
        self.lname = lname

    def instancemethod(self):
        print('Instance method - {}'.format(self))

    @classmethod
    def classmethod(cls):
        print('Class method - {}'.format(cls))

    @staticmethod
    def staticmethod():
        print('Static method')


class Class2:
    class_var = 0

    def __init__(self):
        pass

    def instancemethod(self):
        self.__class__.class_var += 10
        print('{}'.format(self.__class__.class_var))

    @classmethod
    def classmethod(cls):
        print(cls.class_var)


# obj1 = TestClass('John', 'Smith')
# obj1.instancemethod()
# obj1.classmethod()
# obj1.staticmethod()
#
# TestClass.classmethod()
# TestClass.staticmethod()
# # TestClass.instancemethod()  # Can't call a instance method without passing the instance of the class

obj2 = Class2()
Class2.classmethod()
obj2.instancemethod()
Class2.classmethod()
