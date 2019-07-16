import socket as soc

print('The hostname of the box is {}'.format(soc.gethostname()))

HOSTS = ['www.google.com', 'mail.google.com', 'www.python.org']

for host in HOSTS:
    print('{:>20} : {}'.format(host, soc.gethostbyname(host)))
