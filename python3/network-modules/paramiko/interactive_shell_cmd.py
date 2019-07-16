#!/apps/nttech/rbhanot/anaconda3/bin/python

import cmd
import sys


class Demo(cmd.Cmd):
    prompt = '> '

    def do_hello(self, value):
        if value:
            print('Hello ', value)
        else:
            print("hello someone !! ")

    def do_exit(self, line):
        sys.exit('\n Exiting the shell !!\n')


if __name__ == "__main__":
    Demo().cmdloop()
