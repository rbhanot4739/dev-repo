from subprocess import Popen, PIPE

p = Popen(['test.sh'], stdout=PIPE).communicate()[0].decode('utf-8')
print(p)
