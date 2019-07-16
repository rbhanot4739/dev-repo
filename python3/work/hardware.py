# Author: Rohit Bhanot
# Purpose: Started the hardware.py module, with SerialConsoleChecker as first component
# Date: Jan 11, 2018
# Version: 1.0
import re
import time
from getpass import getpass

import pexpect


class MappingError(Exception):
    """
    custom exception to be raised in case there is not entry for host in
    mapping file
    """
    pass


class SerialError(Exception):
    """
    generic exception to be raised when serial console isn't working
    """
    pass


class SerialPasswordError(Exception):
    """
    custom exception to be raised in case of wrong user password
    """
    pass


def serial_console_checker(host=None, pwd=None):
    """
    Checks if the serial console is up or not using pexpect
    :param host: remote hostname
    :param pwd: password
    :return:
        Exception - SerialPasswordError : if the password provided is incorrect
        Exception - SerialError : if we are not able to get the console
        successfully
        string - if console is Okay and hostname status
    """
    host = host or input('Enter the hostname: ')
    pwd = pwd or getpass("Enter password: ")

    try:
        child = pexpect.spawn(f'/usr/local/bin/nprocons -wh {host}', timeout=5)
        child.expect('Password:')
        child.sendline(pwd)
        child.expect('')
        child.sendline()
        time.sleep(2)
        exp = child.expect(['Password:', '.*tower-research.com login:', ':~#'])
        if exp == 0:
            raise SerialPasswordError
        else:
            after = child.after.decode().strip()
            if host in after:
                return "Console Okay, Hostname on machine matches with " \
                       "hostname in Avocent DB"
            else:
                return "Console Okay, Hostname on machine does not match " \
                       "with hostname Avocent DB"
    except (pexpect.exceptions.EOF, pexpect.exceptions.TIMEOUT) as e:
        if re.search(r'could not get session id', str(e)):
            return serial_console_checker(host, pwd)
        elif re.search(r'Could not find Proconsul server for', str(e)):
            raise MappingError
        else:
            raise SerialError
