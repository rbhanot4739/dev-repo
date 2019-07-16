from subprocess import Popen, PIPE
import os

pwd = os.environ["PWD"]
p = Popen(['echo', 'Cureent working directory is', pwd], stdout=PIPE, stderr=PIPE)

# print(p.communicate())
print(p.communicate()[0].decode('utf-8'))
