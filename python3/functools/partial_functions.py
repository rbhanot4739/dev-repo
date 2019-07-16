from functools import partial


def multiplier(x, y):
    print('x is ', x)
    return x*y


multiply5 = partial(multiplier, 5)
multiply8 = partial(multiplier, 8)

print(multiply5(4))
print(multiply8(4))
