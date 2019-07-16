#!/apps/nttech/rbhanot/anaconda3/bin/apython

import paramiko as pk
import cmd
import sys


class SSHShell(cmd.Cmd):
    prompt = 'ssh > '

    def __init__(self):
        cmd.Cmd.__init__(self)
        self.sessions = []

    def do_connect(self, params):
        """Usage connect 'host,user,password' """
        if not params:
            print(self.do_connect.__doc__)
        else:
            data = params.split(",")
            ssh = pk.SSHClient()
            ssh.set_missing_host_key_policy(pk.AutoAddPolicy())
            try:
                ssh.connect(hostname=data[0], username=data[1], password=data[2])
            except pk.AuthenticationException:
                print('Invalid Credentials !!!')
            except pk.SSHException:
                print('Connection could not be made !!')
            else:
                print('Connected to the box, you can run commands now ')
                self.sessions.append(ssh)

    def do_run(self, command):
        """ run <command> """
        if command:
            for ssh in self.sessions:
                stdin, stdout, stderr = ssh.exec_command(command)
                for i in stdout:
                    print(i.strip())
        else:
            print(self.do_run.__doc__)

    def do_close(self, _):
        for ssh in self.sessions:
            ssh.close()

    def do_exit(self, _):
        sys.exit("Exiting the shell !!! ")
        return True


if __name__ == "__main__":
    SSHShell().cmdloop()
