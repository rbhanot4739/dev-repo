from __future__ import print_function
import sys
import os
import getpass
import subprocess as sb
from time import sleep
from socket import gethostname
from helpers import configure_logger, auth_user_from_kerberos


# Declare gloabal variables
logger = configure_logger(__name__, 'decom.log')
host_name = gethostname()
network_scripts_dir = "/etc/sysconfig/network-scripts"
ifguess = None
primary_eth = None


def check_dist_master():
    """
    Check if the server is a dist master
    :return: None
    """
    global host_name
    if sb.call("/usr/local/sbin/global/show_dist_master.sh| awk '{print $2}'| \
                grep -q " + host_name, shell=True) == 0:
        getattr(logger, 'critical')(
            "The server is a Dist Master, please repoint all hosts, Exiting "
            "!!")
        sys.exit(1)
    else:
        getattr(logger, 'info')('Server is not a dist master, continuing ..')


def check_processes(fix):
    """
    Check if there are Trading/Infra processes running on the server
    :return: None
    """
    running_procs_cmd = "ps -eLo pid,ppid,uid,user,comm|grep -v PPID|awk '$3>1000 {print $1}'"
    running_procs = sb.Popen(running_procs_cmd, shell=True, stdout=sb.PIPE,
                             stderr=sb.PIPE).communicate()[0].splitlines()
    if len(running_procs) > 0:
        getattr(logger, 'critical')(
            "There are Trading/Infra processing running on the box, Exiting "
            "!!")
        if not fix:
            sys.exit(1)
        else:
            killcmd = "kill -9 " + ' '.join(running_procs)
            if sb.call(killcmd, shell=True) == 0:
                getattr(logger, 'info')('Processes are killed now, continuing')
    else:
        getattr(logger, 'info')('No critical processes found, continuing ..')


def check_nfs_mounts(fix):
    nfs_mounts = sb.Popen("""awk  '$3=="nfs" {print $2}' /proc/mounts""", shell=True,
                          stdout=sb.PIPE, stderr=sb.PIPE).communicate()[
        0].splitlines()
    if len(nfs_mounts) > 0:
        getattr(logger, 'critical')(
            "Following NFS shares mounted on the server, Exiting !!\n")
        sleep(0.1)
        print('\n'.join(nfs_mounts), '\n')
        if not fix:
            sys.exit(1)
        else:
            try:
                for share in nfs_mounts:
                    print("trying to unmount %s" % share)
                    sb.call("fuser -ck %s" % share, shell=True)
                    sb.call("umount %s" % share, shell=True)
                    getattr(logger, 'info')('NFS shares unmounted'
                                            ' successfully')
            except Exception as e:
                print(e)
                sys.exit(1)
    else:
        getattr(logger, 'info')('No NFS mounts found, continuing ..')


def get_active_interface():
    """
    Find out the active network interface.
    Set to bond0 if exists, otherwise there should only be one ifcfg-eth file
    with ONBOOT=yes
    """
    global ifguess
    global primary_eth
    if os.path.exists("/proc/net/bonding/bond0"):
        interface_count = int(
            sb.Popen("/sbin/ifconfig|egrep '^bond. '|wc -l", stdout=sb.PIPE,
                     shell=True).communicate()[0].strip('\n'))
        if interface_count == 1:
            ifguess = "bond0"
        primary_eth = sb.Popen("/bin/cat /proc/net/bonding/bond0 |grep Active"
                               "|awk '{print $4}'", shell=True,
                               stdout=sb.PIPE).communicate()[0].strip()
    else:
        cmd = 'egrep -l "^ONBOOT=\\"?yes\\"?" ' + network_scripts_dir + \
            '/ifcfg-eth* 2> /dev/null| egrep "ifcfg-eth.$"'
        interface_count = int(
            sb.Popen(cmd + "|wc -l", stdout=sb.PIPE, shell=True).communicate()[
                0].strip('\n'))
        if interface_count > 1:
            getattr(logger, "warning")(
                "More than one interface has ONBOOT=yes.  Exiting.")
            sys.exit(1)
        else:
            ifguess = sb.Popen(cmd, stdout=sb.PIPE, shell=True).communicate()[
                0].splitlines()[0].split('-')[-1]
    if not ifguess:
        getattr(logger, 'error')(
            "Unable to determine active interface. Exiting.")
        sys.exit(1)


def check_vlan(user):
    password = getpass.getpass("Password: ")
    auth_user_from_kerberos(user, password)
    has_acl = sb.Popen("/usr/local/sbin/global/switchport nicget --user=" + user,
                       stdout=sb.PIPE, stdin=sb.PIPE, stderr=sb.PIPE,
                       shell=True).communicate()[0].find(
        "ip access-group public_data_in")

    if has_acl == -1:
        getattr(logger, 'error')(
            "Switch does not have ACL, please ask networks to change the vlan "
            "or do in off hours")
        sys.exit(1)
    else:
        getattr(logger, 'info')(
            "Switch has ACLs on the port, continuing..")


def main(args):
    fix, user = args.fix, args.username
    # check_dist_master()
    check_processes(fix)
    check_nfs_mounts(fix)
    get_active_interface()
    check_vlan(user)
    return (0, ifguess, primary_eth)


if __name__ == "__main__":
    main()
