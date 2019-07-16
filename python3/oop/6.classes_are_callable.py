def generate_seq(n):
    if n:
        cls = tuple
    else:
        cls = list
    return cls


tup = generate_seq(True)
print(type(tup))

t = tup('Hello')
print(t)
print(type(t))

lis = generate_seq(False)
print(type(lis))

l = lis('Hello')
print(l)
