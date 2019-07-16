import os

path = os.environ["PATH"] + ":/root"
env = {"PATH": path, "XYZ": "TEST VAL"}
args = ('world',)

os.execvpe("test.sh", args, env)
