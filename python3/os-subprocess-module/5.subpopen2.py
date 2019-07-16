from subprocess import Popen, PIPE

cmd1 = ['ls', '-l', '/etc']
ls = Popen(cmd1, stdout=PIPE, stderr=PIPE)
wc = Popen(['wc', '-l'], stdin=ls.stdout, stdout=PIPE)

print(wc.communicate()[0].decode('utf-8'))
