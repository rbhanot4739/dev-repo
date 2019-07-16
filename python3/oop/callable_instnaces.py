class A:
    """ Demonstration of class whose instances are callable
        To make a class instance callable, you need to define __call__ method in class definition
     """

    def __init__(self, name):
        self.name = name

    def __call__(self, *args, **kwargs):
        print('Hello ', self.name)


obj = A('World')  # This statement shows that classes are callable as well.
obj()  # Calling the class instance just like a regular callable.
