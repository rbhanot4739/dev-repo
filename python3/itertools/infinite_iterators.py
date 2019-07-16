from itertools import count, cycle, repeat
from time import sleep


# Important thing to remember is to have a exit condition for all these infinite iterators
# otherwise you will run into infinite loop !!


def count_demo():
    """
    Demonstrates itertools.count
    count(start=0, step=1) - Count generates infinite sequence starting with start and optional steps

    """

    for _ in count(10, step=3):
        if _ < 30:
            print(_)
            sleep(0.2)
        else:
            break
    odd_nums = count(1, 2)
    odds = [next(odd_nums) for _ in range(10)]
    print(odds)

def cycle_demo():
    """
    Demonstrates itertools.cycle
    cycle(iterable) - cycles over an iterable infinite number of times.

    """
    counter = 0
    for _ in cycle([2, 1, 4]):
        if counter < 10:
            print(_, end='-')
        else:
            break
        counter += 1



def repeat_demo():
    """
    Demonstrates itertools.repeat
    repeat(object[, times])

    """
    for _ in repeat('abc', 5):
        print(_)

    for _ in repeat([1, 2, 3], 5):
        print(_)


if __name__ == '__main__':
    count_demo()
    # cycle_demo()
    repeat_demo()
