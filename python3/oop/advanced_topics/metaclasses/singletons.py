class SingletonClassException(Exception):
    pass


# class Singleton(type):

#     def __new__(mcs, name, bases, clsdict):
#         clsdict['_objcount'] = 0
#         return super().__new__(mcs, name, bases, clsdict)

#     def __call__(cls, *args, **kwargs):
#         if cls._objcount >= 1:
#             raise SingletonClassException(
#                 "Singleton Class - Only one object can be created")
#         else:
#             cls._objcount += 1
#             return super().__call__()


# A more simpler implementation
class Singleton(type):

    def __new__(mcs, name, bases, clsdict):
        clsdict['_obj'] = None
        return super().__new__(mcs, name, bases, clsdict)

    def __call__(cls, *args, **kwargs):
        print("__call__")
        if cls._obj:
            return cls._obj
        obj = super().__call__()
        cls._obj = obj
        return obj

class Spam(object):
    pass


a = Spam()
b = Spam()


class Junk(metaclass=Singleton):
    pass


x = Junk()
y = Junk()
