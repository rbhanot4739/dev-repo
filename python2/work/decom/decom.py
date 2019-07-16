#!/usr/local/sbin/os/python27

from __future__ import print_function
from time import sleep
from socket import gethostname, gethostbyname
from helpers import configure_logger
import sys
import subprocess as sb
import os
import re


# Declare gloabal variables
logger = configure_logger(__name__, 'decom.log')
host_name = gethostname()
ip = gethostbyname(host_name)
reboot_required = 0
remove_isolcpus = 0
network_scripts_dir = "/etc/sysconfig/network-scripts"


def mark_server_inactive_hwdb():
    global host_name
    global ip
    current_ip = sb.Popen("ip route get 1.1.1.1|awk '/1.1.1.1/ {print $7}'", shell=True,
                          stdout=sb.PIPE).communicate()[0].strip()

    if ip != current_ip:
        getattr(logger, "warning")(
            "Current IP " + current_ip + " is different than the hostname IP "
            + ip)
        sleep(0.1)

    getattr(logger, "info")(
        "Running /usr/local/sbin/os/mark_server_inactive.sh " + host_name)
    sb.call("/usr/local/sbin/os/mark_server_inactive.sh " + host_name,
            shell=True)


def set_vlan(user):
    """
    use switchport nicset to change port to install vlan
    if site is tkp.tower-research.com then install vlan is actually on 121
    and not 21 due to vlan21 being used by Exchange
    """

    match_obj = re.search(r'\.tkp\.?', host_name)
    if match_obj:
        getattr(logger, 'info')("this server is in tkp site,"
                                " so changing port to vlan121("
                                "install vlan for tkp)")
        vlanid = 121
    else:
        getattr(logger, "info")("Changing port to vlan21")
        vlanid = 21

    cmd = "echo 'yes'|/usr/local/sbin/global/switchport nicset {} --user={} "\
          "> /dev/null".format(vlanid, user)
    set_vlan = sb.Popen(cmd, stdout=sb.PIPE, stdin=sb.PIPE, stderr=sb.PIPE,
                        shell=True)

    out, err = set_vlan.communicate()
    print(out)
    if set_vlan.returncode != 0:
        getattr(logger, 'error')("Unable to change switchport, Exiting.")
        sys.exit(1)
    sleep(5)
    # Todo Seems like dummy code
    # renegotiate interfaces for cisco console (set vlan)
    interfaces = sb.Popen("ip link | grep UP| egrep -v 'MASTER|\@' | awk '{print $2}'"
                          " | sed 's/://' | grep -v '^lo$'", stdout=sb.PIPE,
                          shell=True).communicate()[0]
    for intf in interfaces:
        out = sb.Popen("/sbin/ethtool -r" + intf, stdout=sb.PIPE, stderr=sb.PIPE,
                       shell=True).communicate()[0]
    sleep(2)

    for intf in interfaces:
        out = sb.Popen("/sbin/ethtool -r" + intf, stdout=sb.PIPE, stderr=sb.PIPE,
                       shell=True).communicate()[0]
    getattr(logger, 'info')('continuing')


def delete_interface_files(ifguess):
    global reboot_required
    # stop network service
    getattr(logger, 'info')("Stopping network...")
    sb.call("/sbin/service network stop", shell=True)
    sleep(4)

    # remove any meta radio repmux interfaces if exist
    for name in ("meta", "radio", "repmux, mux"):
        for i in "012":
            if os.path.exists(network_scripts_dir + "/ifcfg-" + name + i):
                getattr(logger, 'info')(
                    "rm -f " + network_scripts_dir + "/ifcfg-" + name + i)
                sb.call("rm -f " + network_scripts_dir + "/ifcfg-" + name + i,
                        shell=True)
            reboot_required = 1
    # remove all vlan tagged intefaces
    getattr(logger, 'info')(
        "rm -f " + network_scripts_dir + "/ifcfg-" + ifguess + ".* 2>"
                                                               " /dev/null")
    sb.call("rm -f " + network_scripts_dir + "/ifcfg-" + ifguess + ".* 2> "
                                                                   "/dev/null",
            shell=True)
    # delete the route files
    getattr(logger, 'info')(
        "rm -f " + network_scripts_dir + "/route-* 2> /dev/null")
    sb.call("rm -f " + network_scripts_dir + "/route-*" + " 2> /dev/null",
            shell=True)


def disable_mgmt():
    if sb.call("ip link show | grep mgmt0| egrep 'state UP'", shell=True) == 0:
        getattr(logger, 'info')("Shutting down the management interface mgmt0")
        sb.call("/sbin/ifdown mgmt0", shell=True)
    if os.path.exists(network_scripts_dir + "/ifcfg-mgmt0"):
        getattr(logger, 'info')("Disabling management interface")
        sb.call(
            "sed -i 's/^ONBOOT=yes/ONBOOT=no/' " + network_scripts_dir +
            "/ifcfg-mgmt0", shell=True)
        sb.call(
            "sed -i '/^IPADDR=.*$/d' " + network_scripts_dir + "/ifcfg-mgmt0",
            shell=True)
        sb.call(
            "sed -i '/^NETMASK=.*$/d' " + network_scripts_dir + "/ifcfg-mgmt0",
            shell=True)


def edit_active_interface(ifguess, primary_eth):
    file_name = "/etc/sysconfig/network-scripts/ifcfg-" + ifguess
    getattr(logger, 'info')("Editing %s" % file_name)
    if sb.call('egrep -q "^ONBOOT=\\"?yes\\"?" %s' % file_name, shell=True) != 0:
        getattr(logger, 'error')(
            "ifconfig reports %s as active, but ifcfg-%s doesn't have "
            "ONBOOT=yes. Exiting" % (ifguess, ifguess))
        sys.exit(1)

    # set BOOTPROTO to DHCP
    sed_cmd = "sed -i -e 's/^BOOTPROTO=.*/BOOTPROTO=dhcp/' "

    if sb.call("grep -q '^IPADDR' %s" % file_name, shell=True) == 0:
        sed_cmd += " -e /IPADDR=.*/d "

    if sb.call("grep -q '^NETMASK' %s" % file_name, shell=True) == 0:
        sed_cmd += " -e /NETMASK=.*/d "

    if ifguess == "bond0":
        # remove the kernel bonding module
        getattr(logger, 'info')("Removing the kernel bonding module")
        sb.call("modprobe -r bonding 2> /dev/null", shell=True)
        bonding_opts = '"mode=1-miimon=1000-num_grat_arp=3-primary=%s"' % primary_eth
        if sb.call("grep -q '^BONDING_OPTS' %s" % file_name, shell=True) == 0:
            sed_cmd += " -e 's/BONDING_OPTS=.*/BONDING_OPTS=%s/' " % bonding_opts
        else:
            with open(file_name, "a") as IF:
                IF.write("BONDING_OPTS=%s" % bonding_opts)

        if os.path.exists("/etc/modprobe.conf"):
            sb.call("sed -i  -e /^options\ bonding.*/d /etc/modprobe.conf",
                    shell=True)
    sb.call(sed_cmd + file_name, shell=True)
    # convert dashes (used to "glue" options together while manipulating)
    # back to spaces
    sb.call("sed -i -e /BONDING_OPTS=.*/s/-/\\ /g %s" % file_name, shell=True)

    # edit /etc/sysconfig/network
    getattr(logger, 'info')("Editing /etc/sysconfig/network")
    sb.call("sed -i -e s/^HOSTNAME=.*/HOSTNAME=localhost.localdomain/"
            " /etc/sysconfig/network", shell=True)
    sb.call("sed -i -e /^GATEWAY=.*/d /etc/sysconfig/network", shell=True)


def cleanup_unneccessary_files():
    global remove_isolcpus
    if os.path.exists("/etc/local/passwd"):
        os.remove("/etc/local/passwd")

    if os.path.exists("/etc/cachetop.conf"):
        os.remove("/etc/cachetop.conf")

    if sb.call("grep isolcpus /etc/local/lilo.first", shell=True) == 0:
        sb.call("sed -i -e 's/ isolcpus=[0-9]\{1,2\}\([-,][0-9]\{1,2\}\)*//g' \
                /etc/local/lilo.first", shell=True)
        remove_isolcpus = 1

    # remove non-root crons
    os.chdir("/var/spool/cron")
    getattr(logger, 'info')("Removing non-root cron files")
    for file in os.listdir("."):
        if file != "root":
            os.remove(file)
    os.chdir("/")


def setup_install_host(ifguess):
    # Todo add "echo trade-prod > /var/opt/trc/dist-tree.tag"
    getattr(logger, 'info')("Starting Network services...")
    sb.call("/sbin/service network start > /dev/null", shell=True)
    if sb.call("ping -c 2 -w 5 10.0.20.1 >/dev/null", shell=True) != 0:
        getattr(logger, 'error')("Ping failed, exiting..")
        sys.exit(1)
    # set new hostname
    fqdn = sb.Popen("/sbin/ifconfig %s| sed -rn 's/.*r:([^ ]+) .*/\\1/p' | \
                    /usr/bin/xargs /bin/ipcalc -h | awk -F'=' '{print $NF}'"
                    % ifguess, shell=True, stdout=sb.PIPE).communicate()[0]
    getattr(logger, 'info')("Setting hostname to %s" % fqdn)
    sb.call("hostname %s" % fqdn, shell=True)

    getattr(logger, 'info')("Running triggers now")
    sb.call("/usr/local/sbin/global/run-triggers.pl --all", shell=True)

    getattr(logger, 'info')("Running cdpr.pl via /usr/bin/at")
    sb.call('echo "/usr/local/sbin/global/cdpr.pl" | /usr/bin/at now',
            shell=True)

    # hang up the running getty's so they pick up the new name
    sb.call("killall -1 mingetty", shell=True)
    sb.call("killall -1 agetty", shell=True)

    getattr(logger, 'info')("Removing symlinks from /spare")
    sb.call("find /spare/local /spare/tmp -maxdepth 1 -type"
            " l -exec unlink {} \;", shell=True)
    sb.call("chown -h root.root /spare/local/* /spare/tmp/* 2> /dev/null",
            shell=True)
    sb.call("chmod 700 /spare/local/* /spare/tmp/* 2> /dev/null", shell=True)

    old_host = host_name.replace(".tower-research.com", "")
    new_host = fqdn.replace(".tower-research.com", "")
    mapping_host = "systems1." + new_host.split(".")[-1]

    # remove tags from the server
    sb.call("rm -f /var/local/cf_*", shell=True)
    sb.call("rm -f /var/local/cfengine/*", shell=True)

    getattr(logger, 'info')("Setting the realm of install box to trade-prod")
    sb.call("echo trade-prod > /var/opt/trc/dist-tree.tag", shell=True)

    print("""
    ---------------------------------------------------------------------------
    Server renamed: %s ---> %s
    Please update the mappping file on %s
    Verify if serial console is woriking.
    ---------------------------------------------------------------------------
    """ % (old_host, new_host, mapping_host))

    print("There may be some lingering files in /etc/local that need"
          " to be removed")

    if remove_isolcpus:
        getattr(logger, 'info')("isolcpus settings were removed from \
               this server.")
    if reboot_required:
        print("\nReboot is required !!")


def cleanup_network_config(user, ifguess, primary_eth):
    set_vlan(user)
    delete_interface_files(ifguess)
    disable_mgmt()
    edit_active_interface(ifguess, primary_eth)


def main(args, ifguess, primary_eth):
    user = args.username
    mark_server_inactive_hwdb()
    cleanup_network_config(user, ifguess, primary_eth)
    cleanup_unneccessary_files()
    setup_install_host(ifguess)


if __name__ == "__main__":
    main()
