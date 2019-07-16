#!/usr/bin/python2

import argparse
from fabric.api import *
from getpass import getpass

parser = argparse.ArgumentParser()
site = parser.add_argument('-s', '--site', help="site name")
zone = parser.add_argument('-z', '--zone', help="zone name")

args = parser.parse_args()

if not args.site:
    site = raw_input("Enter the site name: ")
else:
    site = args.site
if not args.zone:
    zone = raw_input("Enter the zone you want to refresh: ")
else:
    zone = args.zone


password = getpass("Enter your sudo password: ")

if site in ['chi-off', 'gurg-off', 'ldn-off', 'ld4-si', 'newark', 'ny',
            'skae']:
    env.hosts = ['systems1.' + site, 'systems2.' + site]
else:
    env.hosts = ['systems1.' + site, 'fileserver1.' + site]
env.password = password


@task
@parallel
def runner():
    if zone.find('tower-research.com') != -1:
        sudo('rndc reload {}.{}'.format(site, zone))
    sudo('rndc reload {}'.format(zone))


with hide('commands'):
    execute(runner)
