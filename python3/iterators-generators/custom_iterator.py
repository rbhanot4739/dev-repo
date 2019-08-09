class PowerGen(object):
    def __init__(self, high):
        self.pow = 1
        self.high = high

    def __iter__(self):
        return self

    def __next__(self):
        if self.pow < self.high:
            result = self.pow ** 2
            self.pow += 1
            return result
        else:
            raise StopIteration


obj = PowerGen(4)
# obj = (x for x in range(3)) # Uncomment to see the difference
i = iter(obj)

print(next(i))
print(next(i))
print(next(i))

i = iter(obj)

print(next(i))
