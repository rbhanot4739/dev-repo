# A Normal class creation

class A:
    def __init__(self):
        pass

    def print(self):
        print("{}".format(type(self)))


a = A()
a.print()


# Class creation using 'type'

def say(self):
    print("Say hello !!")


B = type('B', (A,), {'msg': 'Hello', 'say_hello': say})
b = B()
print(b.msg)
b.say_hello()
