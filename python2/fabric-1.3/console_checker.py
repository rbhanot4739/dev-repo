#!/usr/bn/env python

# Author: Rohit Bhanot
# Purpose: To check if the serial console is working or not
# Date: Jan 04, 2018
# Version: 1.0

import pexpect
from getpass import getpass
from base64 import b64decode
import argparse


def serial_console_checker(host, pwd):
    try:
        child = pexpect.spawn('/usr/local/bin/nprocons -wh %s' % host)
        child.expect('Password:')
        child.sendline(pwd)
        child.expect(' ')
        child.sendline()
        child.expect(['.*login:', ':~#'])
        return "Up"
    except Exception:
        return "Down"


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--machine', '-m', help='Hostname of the remote machine')
    args = parser.parse_args()
    if not args.machine:
        host = raw_input('Enter the hostname: ')
    else:
        host = args.machine
    param = getpass("Enter password: ")
    # param = b64decode(
    #     open('/spare/ssd/rbhanot/nvim/share/nvim/runtime/lua/.config/.config.dat').read())
    for _ in range(2):
        out = serial_console_checker(host, param)
    print("Console is %s" % out)
