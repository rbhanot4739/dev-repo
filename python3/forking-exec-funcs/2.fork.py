import os


def parent():
    while True:
        newpid = os.fork()
        if newpid == 0:
            print("Hello from child", os.getpid(), newpid)
        else:
            print('Hello from parent', os.getpid(), newpid)
        if input() == 0:
            break


parent()
