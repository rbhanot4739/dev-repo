def gen1():
    for i in range(5):
        yield i


g1 = gen1()
print(type(gen1))
print(type(g1))

for _ in g1:
    print(_)


def gen2():
    yield from range(5)


g2 = gen2()

for _ in g2:
    print(_)
