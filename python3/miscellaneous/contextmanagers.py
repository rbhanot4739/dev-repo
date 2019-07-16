import os

from contextlib import contextmanager


# Context Manager mimicking default file opener
#
# class file_opener(object):
#     def __init__(self, file, mode="r"):
#         self.file = file
#         self.mode = mode
#
#     def __enter__(self):
#         self.FILE = open(self.file, self.mode)
#         return self.FILE
#
#     def __exit__(self, exc_type, exc_val, exc_tb):
#         self.FILE.close()
#
#
# with file_opener("/apps/nttech/rbhanot/Documents/Programs/Basics/password_generator.py", "r") as fd:
#     for line in fd:
#         print(line)
#
# print(fd.closed)

class ContextManager(object):
    def __init__(self, dest):
        self.dest = dest

    def __enter__(self):
        print('Running __enter__')
        self.cwd = os.getcwd()
        return os.chdir(self.dest)

    def __exit__(self, exc_type, exc_val, exc_tb):
        print('Running __exit__')
        os.chdir(self.cwd)


@contextmanager
def mydirtraverser(dest):
    cwd = os.getcwd()
    yield os.chdir(dest)
    os.chdir(cwd)


with ContextManager("/apps/nttech") as dir:
    print(os.listdir(dir))  # pass
print(os.listdir(dir))

with mydirtraverser("/spare/ssd/rbhanot") as dir:
    print(os.listdir(dir))

print(os.listdir(dir))
