class Mydict(dict):

    def __init__(self, **key):
        super().__init__()
        for k, v in key.items():
            self[k] = v

    def __setitem__(self, k, val):
        if k in self:
            raise KeyError("Can't modify the value of an existing key")
        else:
            super().__setitem__(k, val)


d = Mydict(a=10, b=20)
print("d = {}".format(d))
