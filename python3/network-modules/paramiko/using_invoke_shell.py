import paramiko as pm
import os

client = pm.SSHClient()
client.set_missing_host_key_policy(pm.AutoAddPolicy())
key_path = os.path.join(os.path.expanduser('~'), '.ssh/id_rsa')
try:
    client.connect(hostname='localhost', username='rbhanot', key_filename=key_path)
except Exception as e:
    print(e)
else:
    shell = client.invoke_shell()
    stdin = shell.makefile('wb')
    stdout = shell.makefile('rb')
    stdin.write('''
    uptime
    exit
    
    ''')

    print(stdout.read().decode())
    # for line in stdout:
    #     print(line.decode().strip())

    stdin.close()
    stdout.close()
    client.close()
