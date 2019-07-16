#!/usr/bin/python

# Rohit Bhanot - 2018/02/22


import os, sys
import subprocess as sb
import difflib
import socket
import argparse
import glob
import shutil


def nic_config_backup(arg):
    config_backup_dir = os.path.join(arg, "nics")
    if not os.path.exists(config_backup_dir):
        os.makedirs(config_backup_dir, mode=0770)
    for file in glob.glob("/etc/sysconfig/network-scripts/ifcfg-*"):
        sb.call(['cp', '-p', file, config_backup_dir])

    with open(os.path.join(config_backup_dir, "link-status"), "w") as OF:
        output = sb.Popen(
            """/usr/local/sbin/os/nic_list.pl |awk '{print $1"\t"$3"\t"$7}'""",
            shell=True, stdout=sb.PIPE).communicate()[0]
        OF.write(output)


def route_config_backup(arg):
    config_backup_dir = os.path.join(arg, "routes")
    if not os.path.exists(config_backup_dir):
        os.makedirs(config_backup_dir, mode=0770)
    # Taking back up of static route files
    for file in glob.glob("/etc/sysconfig/network-scripts/route-*"):
        sb.call(['cp', '-p', file, config_backup_dir])

    # Taking backup of dynamic routes
    cmd = ['ip r| sort | egrep -v "zebra|169.254"']
    routes = \
    sb.Popen(cmd, stdout=sb.PIPE, stderr=sb.PIPE, shell=True).communicate()[0]
    route_file = os.path.join(config_backup_dir, "routes")
    with open(route_file, 'w') as OF:
        OF.writelines(routes)


def crontabs_backup(arg):
    config_backup_dir = os.path.join(arg, "crontabs")
    if not os.path.exists(config_backup_dir):
        os.makedirs(config_backup_dir, mode=0770)
    # Taking back up of crontabs
    for file in os.listdir("/var/spool/cron"):
        sb.call(['cp', '-p', os.path.join("/var/spool/cron", file),
                 config_backup_dir])


def get_lldp_neighbour_backup(arg):
    file = arg + '/lldp_neighbours_config'
    host_name = socket.gethostname().replace('.tower-research.com', '')
    cmd = ['/usr/local/sbin/os/get_salt_lldp.py', host_name]
    lldp_info = sb.Popen(cmd, stdout=sb.PIPE, stderr=sb.PIPE).communicate()[0]
    with open(file, "w") as OF:
        OF.write(lldp_info)


def get_file_config_backup(DIR_PATH, arg):
    file = os.path.join(DIR_PATH, arg)
    arg = "/" + arg.replace("-", "/")
    output = \
    sb.Popen(['/bin/cat', arg], stdout=sb.PIPE, stderr=sb.PIPE).communicate()[
        0]
    with open(file, 'w') as OF:
        OF.writelines(output)


def get_dimms_backup(arg):
    file = arg + '/dimms-backup'
    output = \
    sb.Popen(['/usr/local/bin/lsdimms'], stdout=sb.PIPE).communicate()[
        0].decode().split('\n')[:-1]
    with open(file, "w") as OF:
        for i in output:
            l = i.split(',')
            OF.write(l[1] + ' ' + l[0] + ' ' + l[4] + '\n')


def get_kernel_cmdline_backup(arg):
    file = arg + '/kernel-cmdline'
    kernel = sb.Popen(['/bin/uname', '-r'], stdout=sb.PIPE).communicate()[0]
    cmdline = \
    sb.Popen(['/bin/cat', '/proc/cmdline'], stdout=sb.PIPE).communicate()[
        0].replace('auto', '')
    with open(file, "w") as OF:
        OF.write(kernel)
        OF.write(cmdline)


def output_header(config_path):
    text = "Config changes for %s" % config_path.capitalize()
    # print '\n', '~' * 70
    print  text.center(50, '~')  # print  '\n' ,'~' * 70


def differ(config_path, show_header):
    with open(os.path.join(FS_PATH, "prereboot", config_path)) as IF:
        preboot = sorted((line.lower() for line in IF))

    with open(os.path.join(FS_PATH, "postreboot", config_path))as IF:
        postboot = sorted((line.lower() for line in IF))

    lines_removed = '\t'.join(
        x.lstrip('-') for x in difflib.ndiff(preboot, postboot) if
        x.startswith('-'))
    lines_added = '\t'.join(
        x.lstrip('+') for x in difflib.ndiff(preboot, postboot) if
        x.startswith('+'))

    if lines_added or lines_removed:

        if not show_header:
            output_header(config_path.split('/')[0])
            show_header = 1

        print '\n*** Changes in the file', config_path, '***'

        if lines_removed:
            print "Before reboot"
            print '\t' + lines_removed,
        if lines_added:
            print "After reboot"
            print '\t' + lines_added,
    return show_header


def config_diff(FS_PATH, config_parameter):
    if os.path.isdir(os.path.join(FS_PATH, "prereboot", config_parameter)):
        pre_reboot_files = os.listdir(
            os.path.join(FS_PATH, "prereboot", config_parameter))
        post_reboot_files = os.listdir(
            os.path.join(FS_PATH, "postreboot", config_parameter))
        common_files = [f1 for f1 in pre_reboot_files for f2 in
                        post_reboot_files if f1 == f2]
        files_deleted = [f for f in pre_reboot_files if
                         f not in post_reboot_files]
        files_added = [f for f in post_reboot_files if
                       f not in pre_reboot_files]
        show_header = 0

        if files_added or files_deleted:
            show_header = 1
            output_header(config_parameter)

            if files_deleted:
                print "\n", '-' * 5, "Files removed after reboot", '-' * 5
                print ('\t' + '\n\t'.join(files_deleted))

        if files_added:
            print "\n", '+' * 5, "Files added after reboot", '+' * 5
            print ('\t' + '\n\t'.join(files_added))

        for file in common_files:
            config_path = config_parameter + "/" + file
            show_header = differ(config_path, show_header)
    else:
        show_header = 0
        differ(config_parameter, show_header)


if __name__ == '__main__':

    host = socket.gethostname()


    # if "install" in host or "localhost" in host:
    #     sys.exit(0)

    def usage():
        return """configbackup.py [-h] {pre,post,alert}
            where
            pre     - capture the server configuration before the reboot
            post    - capture the server configuration after the reboot
            alert   - compare pre and post configurations
        """


    parser = argparse.ArgumentParser(
        description="Take backup of system configurations", usage=usage())
    parser.add_argument("val", choices=['pre', 'post', 'alert'],
                        help="Please enter pre,post or alert")
    args = parser.parse_args()

    configs_to_monitor = (
        'nics', 'routes', 'lldp_neighbours_config', 'crontabs', 'etc-passwd',
        'etc-fstab', 'etc-precious', 'dimms-backup', 'kernel-cmdline')
    FS_PATH = "/spare/tmp"
    if args.val != "alert":

        if args.val == "pre":
            DIR_PATH = os.path.join(FS_PATH, "prereboot")
        if args.val == "post":
            DIR_PATH = os.path.join(FS_PATH, "postreboot")

        if os.path.exists(DIR_PATH):
            shutil.rmtree(DIR_PATH)

        # print ("Creating the config backup at %s" % DIR_PATH)
        os.makedirs(DIR_PATH)

        for item in configs_to_monitor:
            if "etc" in item:
                get_file_config_backup(DIR_PATH, item)

        nic_config_backup(DIR_PATH)
        route_config_backup(DIR_PATH)
        crontabs_backup(DIR_PATH)
        get_lldp_neighbour_backup(DIR_PATH)
        get_dimms_backup(DIR_PATH)
        get_kernel_cmdline_backup(DIR_PATH)

    else:
        if (os.path.exists(FS_PATH + "/prereboot")) and (
        os.path.exists(FS_PATH + "/postreboot")):
            for item in configs_to_monitor:
                config_diff(FS_PATH, item)
        else:
            pass
