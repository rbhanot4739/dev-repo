import os

dir_list = os.popen("ls -l")
print(dir_list.read())
