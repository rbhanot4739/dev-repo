class PrimeGenerator(object):
    def __init__(self, high):
        self.num = 0
        self.is_prime = 0
        self.high = high

    def __iter__(self):
        num = 0
        flag = False
        while num < 10:
            if num > 2:
                for i in range(2, num):
                    if num % i == 0:
                        flag = True
                        break

                if flag is not True:
                    yield num
            else:
                yield num

            flag = False
            num += 1


def prime_square(primes):
    print(id(primes))
    squares = map(lambda x: x ** 2, primes)
    cubes = map(lambda x: x ** 3, primes)

    for i in squares:
        print(i)
    print('-------')
    for i in cubes:
        print(i)


p = PrimeGenerator(10)

print(iter(p) is iter(p))

prime_square(p)
prime_square(p)
