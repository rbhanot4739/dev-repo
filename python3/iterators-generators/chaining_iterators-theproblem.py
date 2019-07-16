def prime_generator():
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


def prime_list():
    num = 0
    flag = False
    primes = []
    while num < 10:
        if num > 2:
            for i in range(2, num):
                if num % i == 0:
                    flag = True
                    break

            if flag is not True:
                primes.append(num)
        else:
            primes.append(num)

        flag = False
        num += 1

    return primes


list_primes = prime_list()
gen_primes = prime_generator()


def prime_square(primes):
    squares = map(lambda x: x ** 2, primes)
    cubes = map(lambda x: x ** 3, primes)

    for i in squares:
        print(i)
    print('-------')
    for i in cubes:
        print(i)


print("Generator Version")
prime_square(gen_primes)
print('List Version')
prime_square(list_primes)
