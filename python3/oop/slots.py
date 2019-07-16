class Test1:
    def __init__(self, a, b):
        self.a = a
        self.b = b


class Test2:
    __slots__ = ['x', 'y']

    def __init__(self, a, b):
        self.x = a
        self.y = b


test1 = Test1(10, 20)
print(test1.__dict__)
test1.c = 30
test1.d = 40
print(test1.__dict__)

test2 = Test2(100, 200)
print(test2.__slots__)
test2.i = 300
