### http://www.csl.mtu.edu/cs4411.ck/www/NOTES/process/fork/create.html ## 

# Please note that Unix will make an exact copy of the parent's address space and give it to the child. Therefore, the parent and child processes have separate address spaces. 

#	If fork() returns a negative value, the creation of a child process was unsuccessful.
#	fork() returns a zero to the newly created child process.
#	fork() returns a positive value, the process ID of the child process, to the parent
#	When the main program executes fork(), an identical copy of its address space, including the program and all data, is created. System call fork() returns the child process ID to the parent and returns 0 to the child process.

import os


def child():
    print('\nA new child ', os.getpid())
    os._exit(0)


def parent():
    while True:
        newpid = os.fork()
        if newpid == 0:
            child()
        else:
            print("parent: {}, child: {}".format(os.getpid(), newpid))
        reply = input("q for quit / c for new fork")
        if reply == 'c':
            continue
        else:
            break


parent()
