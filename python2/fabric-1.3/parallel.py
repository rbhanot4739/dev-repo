#!/usr/bin/python2


from fabric.api import *
import sys

env.hosts = sys.argv[1:]


@task
# @parallel
def runner():
    run("uname -mrs")


# with hide('running'):
execute(runner)
