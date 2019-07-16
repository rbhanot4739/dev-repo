import sys
from time import sleep


def fib_gene():
    first, second = 10, 11
    while True:
        yield first + second
        first, second = second, first + second
        sleep(0.09)


for i in fib_gene():
    print(i)  # if i < 20000:  #     print(i)  # else:  #     sys.exit(0)
