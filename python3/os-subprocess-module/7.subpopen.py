from subprocess import Popen, PIPE
import sys

cmd1 = ['/usr/bin/python3.5', '0.sys.py', ' '.join(sys.argv[1:])]

proc = Popen(cmd1, stdout=PIPE, stderr=PIPE, stdin=PIPE)
# proc=Popen(cmd1,cwd='/root',stdout=PIPE,stderr=PIPE,stdin=PIPE) # with cwd- Current Working directory set to /root
print(proc.communicate()[0].decode())
