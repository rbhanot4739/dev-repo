#!/usr/local/sbin/os/python27

from argparse import ArgumentParser
import pre_checks
import decom

parser = ArgumentParser(description="command line arguements for \
                            decommissioning")
parser.add_argument("-u", "--username", required=True)
parser.add_argument("-f", "--fix", help="fix the errors automatically",
                    action="store_true")
args = parser.parse_args()

# Do the pre_checks first
ret_code, ifguess, primary_eth = pre_checks.main(args)

if ret_code == 0:
    print "\nAll pre_checks done successfully\n"
    decom.main(args, ifguess, primary_eth)
