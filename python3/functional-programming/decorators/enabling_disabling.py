class A():
    def __init__(self):
        self.logging = True

    def __call__(self, f, *args, **kwargs):
        def wrap(*args, **kwargs):
            if self.logging:
                print('Started logging for the {}'.format(f.__name__))
            return f()

        return wrap


@A()  # you can either do @A() or a = A() and then decorate with @a
def hello():
    return 'Hello'
