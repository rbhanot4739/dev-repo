import os

env = {"PATH": "/root", "XYZ": "TEST VAL"}
args = ('world',)

os.execvpe("test.sh", args, env)
