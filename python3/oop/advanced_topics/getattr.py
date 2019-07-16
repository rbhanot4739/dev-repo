class A:

    def __init__(self, a, b):
        self.a = a
        self.b = b

    def __getattribute__(self, name):
        print("__getattribute__ will be called for every attribute")
        return super().__getattribute__(name)

    def __getattr__(self, name):
        print(f"{name} does not exist")
        return getattr(self, "a")
