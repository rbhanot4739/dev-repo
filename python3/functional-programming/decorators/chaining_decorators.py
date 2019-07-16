# def star(func):
#     def inner(*args, **kwargs):
#         print("*" * 60)
#         func(*args, **kwargs)
#         print("*" * 60)
#
#     return inner

def quoter(punc):
    def percent(func):
        def inner(*args, **kwargs):
            print(punc * 60)
            func(*args, **kwargs)
            print(punc * 60)

        return inner

    return percent


tag1 = input('Enter 1st punctuation mark: ')
tag2 = input('Enter 2nd punctuation mark: ')


# @star
@quoter(tag2)
@quoter(tag1)
def printer(*args, **kwargs):
    print(args, kwargs)


printer("Hello", "How are you", name="Rohit")
