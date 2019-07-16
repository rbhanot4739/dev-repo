from functools import wraps


def func_counter(func):

    @wraps(func)
    def counter(*args):
        res = func(*args)
        counter.count += 1
        return res

    counter.count = 0
    return counter


# @func_counter
# def greet(*args):
#     return 'Hello {}'.format(' '.join(args))
#

# greet()
# greet()
# greet()

@func_counter
def bye(*args):
    return 'Bye {} !!'.format(' '.join(args))


if __name__ == '__main__':
    bye('a')
    bye('b')
    print(bye.count)
