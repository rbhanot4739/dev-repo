def decorator(args):
    def real_decorator(func):
        def wrapper(*test):
            print("Decorating the function with {}".format(args))
            for name in test:
                print("<{1}> {0} </{1}>".format(func(name), args))
            print("Function has been decorated")

        return wrapper

    return real_decorator


@decorator('div')
def tags(name):
    return name


tags("Sample text1", "Sample text2")
