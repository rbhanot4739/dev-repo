from subprocess import Popen, PIPE

ls = Popen(['ls', '-l'], stdout=PIPE)
wc = Popen(['wc', '-l'], stdin=ls.stdout, stdout=PIPE)
print(wc.communicate()[0].decode('utf-8'))
