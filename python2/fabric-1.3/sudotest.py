import fabric.api as fab

fab.env.hosts = ['install190.gurg-off', 'install035.mumbai-off']
# env.passwords = []

# @fab.parallel
def test():
    fab.run("uname -a")
