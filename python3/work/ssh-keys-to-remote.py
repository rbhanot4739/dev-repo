#!/usr/bin/env python

from __future__ import print_function
import sys
import time
import argparse
import os
import pexpect
import fabric
from subprocess import Popen, PIPE
from getpass import getuser
from threading import Thread

try:
    from queue import Queue
except ImportError:
    from Queue import Queue


def setup_remote_host(h):
    global pwd
    with fabric.group.ThreadingGroup(
            *h, user=getuser(), connect_kwargs={'password': pwd}) as c:
        c.run("chmod 700 ~/")
        c.run("[ -d ~/.ssh ] && chmod 700 ~/.ssh/")
        c.run(
            "[ -f ~/.ssh/authorized_keys ] && chmod 600 ~/.ssh/authorized_keys"
        )  # c.run("cat /dev/null >| ~/.ssh/authorized_keys")


def copy_ssh_keys(q, s):
    global pwd
    try:
        while True:
            host = q.pop()
            try:
                child = pexpect.spawn('ssh-copy-id {}'.format(host))
                child.expect('.*assword:')
                child.sendline(pwd)
                child.expect(pexpect.EOF, timeout=None)
                print('Copied ssh-keys on -> {}'.format(host))
            except Exception:
                print('Looks like ssh-keys have already been '
                      'setup for {} -> Skipping ..'.format(host))
    except IndexError:
        pass


if __name__ == '__main__':
    try:
        start = time.time()
        parser = argparse.ArgumentParser()
        parser.add_argument(
            '-s',
            '--setup',
            default=False,
            action="store_true",
            help="Setup remote hosts with appropriate settings")
        args = parser.parse_args()

        hosts = Popen(
            "/usr/local/sbin/os/get-cdp -_ systems1%|egrep -v "
            "'old|windows|repo|oob|systemsdb|hostname'",
            shell=True,
            stdout=PIPE).communicate()[0].decode().splitlines()

        pwd = os.environ.get('PASSWD', None)
        if pwd is None:
            sys.exit(
                '\nNo Password found in shell env\n'
                '\nPlease do "export PASSWD=<yourPassword>" and run the script again.\n'
            )
        if args.setup:
            setup_remote_host(hosts)
        threads = [
            Thread(target=copy_ssh_keys, args=(hosts, args.setup))
            for _ in range(20)
        ]

        for th in threads:
            th.daemon = True
            th.start()

        for th in threads:
            th.join()
        print('Time Taken {:.3f} seconds'.format(time.time() - start))
    except KeyboardInterrupt:
        sys.exit('Ctrl-c issued by user .. Exiting')
