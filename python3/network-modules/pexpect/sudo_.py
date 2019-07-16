import pexpect
from getpass import getpass

pwd = getpass("password: ")

child = pexpect.spawn('sudo cat /etc/shadow')
child.expect('.*ssword.*:')
child.sendline(pwd)
child.expect(pexpect.EOF, timeout=None)
cmd_show_data = child.before
cmd_output = cmd_show_data.split('\r\n')
for data in cmd_output:
    print(data)
