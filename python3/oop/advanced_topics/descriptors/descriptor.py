# https://docs.python.org/3.6/howto/descriptor.html

# class Function(object):
#     
#     def __get__(self, obj, objtype=None):
#         "Simulate func_descr_get() in Objects/funcobject.c"
#         if obj is None:
#             return self
#         return types.MethodType(self, obj)

# class ClassMethod(object):
#     "Emulate PyClassMethod_Type() in Objects/funcobject.c"

#     def __init__(self, f):
#         self.f = f

#     def __get__(self, obj, klass=None):
#         if klass is None:
#             klass = type(obj)
#         def newfunc(*args):
#             return self.f(klass, *args)
#         return newfunc

# class StaticMethod(object):
#     "Emulate PyStaticMethod_Type() in Objects/funcobject.c"

#     def __init__(self, f):
#         self.f = f

#     def __get__(self, obj, objtype=None):
#         return self.f



class A:
    def __init__(self, func):
        self.func = func
    
    def __get__(self, instance, owner):
        if instance is None:
            return self.func.__get__(owner(), owner)
        return self.func.__get__(instance, owner)


class B:

    def hello(self):
        print("Hello")

    # @A
    def bye(self):
        print("Bye")
    
    bye = A(bye)