from subprocess import Popen, PIPE

p=Popen(['cat', '-'],stdin=PIPE,stdout=PIPE)

msg = b'Input to shell command via Popen\n'
#  print(p.communicate(msg)[0].decode('utf-8'))
out = p.communicate(msg)[0]
print(out)
