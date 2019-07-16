class NumbersIterator(object):
    def __init__(self, nums):
        self.nums = nums
        self.length = len(self.nums)
        self.counter = 0

    def __next__(self):
        if self.counter < self.length:
            self.value = self.nums[self.counter]
            self.counter += 1
            return self.value
        else:
            raise StopIteration


class NumbersIterable(object):
    def __init__(self, *nums):
        self.nums = nums

    def __iter__(self):
        return NumbersIterator(self.nums)


class LettersIterator(object):
    def __init__(self, *letters):
        self.letters = letters
        self.length = len(self.letters)
        self.counter = 0

    def __iter__(self):
        return self

    def __next__(self):
        if self.counter < self.length:
            self.value = self.letters[self.counter]
            self.counter += 1
            return self.value
        else:
            raise StopIteration


numObj = NumbersIterable(1, 2)

iter_obj1 = iter(numObj)
iter_obj2 = iter(numObj)

print(next(iter_obj1))
print(next(iter_obj1))

print(next(iter_obj2))
print(next(iter_obj2))

letterObj = LettersIterator('a', 'b')

iter_obj1_ltr = iter(letterObj)
iter_obj2_ltr = iter(letterObj)

print(next(iter_obj1_ltr))
print(next(iter_obj1_ltr))

print(next(iter_obj2_ltr))
print(next(iter_obj2_ltr))
