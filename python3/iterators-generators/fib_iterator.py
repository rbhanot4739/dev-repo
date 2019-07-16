class fibIter(object):

    def __init__(self, number):
        self.number = number
        self.first = 0
        self.second = 1

    def __iter__(self):
        self.n = 1
        return self

    def __next__(self):
        if self.n < self.number:
            self.third = self.first + self.second
            self.first, self.second = self.second, self.third
            self.n += 1
            return self.third
        else:
            raise StopIteration


fib = fibIter(10)

for i in fib:
    print(i)
