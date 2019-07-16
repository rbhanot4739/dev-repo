# You can run the cProfiler from within your code to profile individual fxns like below
# cProfile.run(func_name)

from time import sleep


def slow():
    print('Sleeping !!')
    sleep(10)
    print('Waking up !!')


def fast():
    print('Executing the fast function')


slow()
fast()  # cProfile.run('slow()')
