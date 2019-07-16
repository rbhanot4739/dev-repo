#!/apps/nttech/rbhanot/anaconda3/bin/python

import paramiko
from sys import argv

data1 = argv[1]
data2 = argv[2]

# Connecting to the host
client = paramiko.SSHClient()

# Loading the host keys from file.

# client.load_host_keys("/apps/nttech/rbhanot/.ssh/known_hosts")
# client.load_system_host_keys()

client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
# client.set_missing_host_key_policy(paramiko.WarningPolicy())

# client.connect(hostname="systems1.gurg-dc", username=data1, key_filename="/apps/nttech/rbhanot/.ssh/id_rsa")`
client.connect(hostname="rbhanotlinux.gurg-off.tower-research.com", username=data1, password=data2)

# Executing commands over the connected session

stdin, stdout, stderr = client.exec_command("cd /etc")

for file in stdout:
    print(file.strip())

stdin, stdout, stderr = client.exec_command("ls -l")

for file in stdout:
    print(file.strip(), '**')

client.close()
