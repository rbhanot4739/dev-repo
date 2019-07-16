class A():
    def __init__(self, f):
        self._f = f

    def __call__(self, *args, **kwargs):
        print('Decorating the function')
        res = self._f(*args, **kwargs)
        print(res)
        print('Done')


@A
def list_flattner(l):
    flattened = []
    for elem in l:
        if not isinstance(elem, list):
            flattened.append(elem)
        else:
            flattened.extend(elem)
    return flattened


l = [1, 2, 3, ['q', 'y', 'z'], [32], [7, [5, 34, 6], 5], 90]
list_flattner(l)
