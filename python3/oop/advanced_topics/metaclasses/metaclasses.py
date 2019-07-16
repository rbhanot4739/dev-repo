class MyMeta(type):

    @classmethod
    def __prepare__(mcs, clsname, bases, **kwargs):
        print(
            "{0} Invoking __prepare__ -> {1}.__prepare__ {0}".format('*' * 20,
                                                                     mcs.__name__))
        print("mcs = {}".format(mcs))
        print("Name of the class being created = {}".format(clsname))
        print("Tuple of base classes = {}".format(bases))
        clsdict = super().__prepare__(mcs, clsname, bases)
        print("Class namespace = {}".format(clsdict))
        return clsdict

    def __new__(mcs, clsname, bases, clsdict):
        print("{0} Invoking __new__ -> {1}.__new__ {0}".format('*' * 20,
                                                               mcs.__name__))
        print("mcs = {}".format(mcs))
        print("Name of the class being created = {}".format(clsname))
        print("Tuple of base classes = {}".format(bases))
        print("Class namespace = {}".format(clsdict))
        upper_case = {(k.upper() if not k.startswith('__') else k): v for k, v
                      in clsdict.items()}
        cls = super().__new__(mcs, clsname, bases, upper_case)
        print("Class created = {}".format(cls))
        return cls

    def __call__(cls, *args, **kwargs):
        print("\n{0} Invoking __call__ -> {1}.__call__ {0}".format('*' * 20,
                                                                   cls.__name__))
        ins = super().__call__()
        print(ins)
        return ins


class Spam(metaclass=MyMeta):
    foo = 'bar'

    def __new__(cls, *args, **kwargs):
        print('===== Invoking {}.__new__ ====='.format(cls.__name__))
        return super().__new__(cls)

    def __init__(self):
        self.x = 1
        print("===== Invoking {}.__init__ ======".format(
            self.__class__.__name__))


obj = Spam()

print(hasattr(obj, 'foo'))
print(hasattr(obj, 'FOO'))
