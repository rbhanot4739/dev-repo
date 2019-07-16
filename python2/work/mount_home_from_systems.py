#!/usr/bin/python

import sys
import os
import subprocess
import socket
import datetime
import time
import shutil
import getopt
import re

snap_mt = "/n/systems1/homesnaps"
lv = "fileserver1_lv"


# Check this script runs from Systems server
def check_system_server():
    myhost = os.uname()[1]
    if not ("systems1" in myhost):
        print "!!!!Script needs to be run on systems server"
        sys.exit(1)


def get_dns_domain():
    return socket.getfqdn().split('.', 2)[1]


# print get_dns_domain()


# Check the systems1_vg on Systems server
def check_systems_vg():
    vg = subprocess.Popen(["vgs systems1_vg"], stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                          shell=True)
    out, err = vg.communicate()
    # print "Checking Required VG for creating filesystem exists"
    out = str(out)
    if vg.returncode != 0:
        print err
        sys.exit(1)


# Check homesnaps mount exists or not
def check_homesnaps_mt():
    df = subprocess.Popen(
        ['df', '-h'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out, err = df.communicate()
    pattern = out
    # print "Checking snapshot"+" "+snap_mt+"exists"
    if not (snap_mt in pattern):
        print "ERROR" + " " + snap_mt + "snap mount doesn't exist"
        sys.exit(1)


def get_lvs():
    lvm = subprocess.Popen(
        ["lvs"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out, err = lvm.communicate()
    out = out.splitlines()
    lvs = []
    for line in out:
        lvs.append(line.split()[0])

    return lvs


def create_lvm():
    lvs = get_lvs()
    if lv in lvs:
        print "ERROR" + " " + lv + \
            "LV already exists, please check you are not creating an existing LV"
        sys.exit(1)
    lvc = subprocess.Popen(["lvcreate -L 100g -n fileserver1_lv systems1_vg"],
                           stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    out, err = lvc.communicate()
    # print Creating Filesystem for snapshot mount point
    if lvc.returncode != 0:
        print "ERROR:" + " " + err
        sys.exit(1)
    else:
        mkfs = subprocess.Popen(["mkfs.xfs /dev/systems1_vg/fileserver1_lv"],
                                stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
        out, err = mkfs.communicate()
        if mkfs.returncode != 0:
            print "ERROR:" + " " + err
            sys.exit(1)
    src = "/etc/fstab"
    dst = '/etc/fstab%s-' % datetime.datetime.now()
    # print "Taking backup of /etc/fstab file"
    shutil.copy2(src, dst)
    fs_mnt = "/dev/systems1_vg/fileserver1_lv"
    fs = open(src, "r")
    content = fs.read().replace('\n', "")
    if fs_mnt in content:
        pass
    else:
        f = open(src, 'a')
        f.write(
            '/dev/systems1_vg/fileserver1_lv /n/fileserver1 xfs noatime,usrquota,nosuid,nodev 0 0\n')
        f.close()
    mnt = "/n/fileserver1"
    if not os.path.isdir(mnt):
        os.makedirs(mnt)
    mount = subprocess.Popen(["/bin/mount" + " " + mnt], stdout=subprocess.PIPE,
                             stderr=subprocess.PIPE, shell=True)
    out, err = mount.communicate()
    # print "Mounting"+ " " +mnt
    if mount.returncode != 0:
        print "ERROR:" + " " + err
    domain = get_dns_domain()
    snap = "/n/systems1/homesnaps/hourly.0/fileserver1" + "." + domain
    link = "/n/fileserver1/home"
    snap_dir = subprocess.Popen(['ls -l' + " " + snap], stdout=subprocess.PIPE,
                                stderr=subprocess.PIPE, shell=True)
    out, err = snap_dir.communicate()
    # print "Making link with latest snapshot file"
    if snap_dir.returncode != 0:
        print "ERROR:" + " " + err
    else:
        os.symlink(snap, link)
    export_s = "/n/fileserver1/home 10.0.0.0/8(rw,sync,no_root_squash,no_subtree_check)"
    export_f = "/etc/exports"
    dexports_f = '/etc/exports%s-' % datetime.datetime.now()
    # print Taking backup of /etc/exports file
    shutil.copy2(export_f, dexports_f)
    f = open(export_f, 'r')
    exportf = f.read().replace('\n', "")
    if export_s in exportf:
        pass
    else:
        f = open(export_f, 'a')
        #	print "Updating /etc/exports file"
        f.write(export_s + '\n')
        f.close()
    run_exportfs = subprocess.Popen(['exportfs -r'], stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                    shell=True)
    out, err = run_exportfs.communicate()
    if run_exportfs.returncode != 0:
        print "ERROR:" + " " + err


def plumb_fs1_ip():
    FS_IP = socket.gethostbyname("fileserver1." + get_dns_domain())
    subprocess.call(["ifconfig", "bond0:1", FS_IP])


def updatecron():
    file = "/var/spool/cron/root"
    snapshot = "/usr/local/sbin/os/rsnapshot-homes-wrapper.sh"
    # print "Updating Cron to disable snaphots"
    with open(file, 'r') as f:
        lines = f.readlines()

    with open(file, 'w') as f:
        for a in lines:
            if snapshot in a:
                if re.match('#', a):
                    pass
                else:
                    a = '#' + a
            f.writelines(a)


def rollback():
    file = "/var/spool/cron/root"
    snapshot = "/usr/local/sbin/os/rsnapshot-homes-wrapper.sh"
    # print "INFO: Checking root cron for rshapshot is disabled or not"
    with open(file, "r") as f:
        lines = f.readlines()

    with open(file, 'w') as f:
        for a in lines:
            if snapshot in a:
                if re.match('#', a):
                    a = a[1:]
            f.writelines(a)
    export_s = "/n/fileserver1/home 10.0.0.0/8(rw,sync,no_root_squash,no_subtree_check)"
    export_f = "/etc/exports"
    dexports_f = '/etc/exports%s-' % datetime.datetime.now()
    shutil.copy2(export_f, dexports_f)
    with open(export_f, "r") as f:
        lines = f.readlines()

    with open(export_f, "w") as f:
        for a in lines:
            if a != export_s + "\n":
                f.write(a)

    run_exportfs = subprocess.Popen(['exportfs -r'], stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                    shell=True)
    out, err = run_exportfs.communicate()
    if run_exportfs.returncode != 0:
        print "ERROR:" + " " + err

    link = "/n/fileserver1/home"
    if os.path.exists("/n/fileserver1/home"):
        os.unlink(link)
    else:
        pass

    mt = "/n/fileserver1"
    df = subprocess.Popen(
        ['df', '-h'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out, err = df.communicate()
    pattern = out
    # print "INFO: Checking snapshot mount "+" "+mt+"exists"
    if mt in pattern:
        # print "cleaning mount point"+" "+mt
        umount = subprocess.Popen(["/bin/umount" + " " + mt], stdout=subprocess.PIPE,
                                  stderr=subprocess.PIPE, shell=True)
        out, err = umount.communicate()
        if umount.returncode != 0:
            print "ERROR:" + " " + err
    else:
        pass

    if os.path.exists("/n/fileserver1"):
        os.system("/bin/rm -r /n/fileserver1")
    else:
        print "INFO: Mount /n/fileserver1 doesn't exist \n"

    src = "/etc/fstab"
    dst = '/etc/fstab%s-' % datetime.datetime.now()
    shutil.copy2(src, dst)
    fs_mnt = "/dev/systems1_vg/fileserver1_lv /n/fileserver1 xfs noatime,usrquota,nosuid,nodev 0 0"
    with open(src, "r") as f:
        lines = f.readlines()

    with open(src, 'w') as f:
        for a in lines:
            if a != fs_mnt + "\n":
                f.write(a)

    lvs = get_lvs()
    if lv in lvs:
        lvr = subprocess.Popen(["lvremove -f /dev/systems1_vg/fileserver1_lv"],
                               stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
        out, err = lvr.communicate()
        if lvr.returncode != 0:
            print "ERROR:" + " " + err
    else:
        pass


def usage():
    print """Usage: mount_home_from_systems.py [--help] [--rollout=r] [--backout=b]

--help           show help
--rollout        rollout the mount home from Systems Server
--backout 	 rollback the changes once fileserver is back online

Must be run on systems server.
"""


def main():
    try:
        opts, args = getopt.getopt(sys.argv[1:], "hrb", [
                                   "help", "rollout", "backout"])
    except:
        usage()
        sys.exit(2)

    for opt, arg in opts:
        if opt in ("-h", "--help"):
            usage()
            sys.exit()
        elif opt in ("-r", "--rollout"):
            print "Preparing System for mounting Home from Systems Snaphot!!!!\n"
            check_system_server()
            check_systems_vg()
            check_homesnaps_mt()
            get_dns_domain()
            create_lvm()
            updatecron()
            print "INFO:Home Mount from System's server is ready \n"
            print "INFO: Test on some Install box that you are able to mount it properly\n"
            print "For Example: install093.jc:~# mount anvil.jc.tower-research.com:/n/fileserver1/home /mnt\n"
            print """INFO: if above mount works fine, then 
            go to your cfengine repo masterfiles/templates/automount

            vi auto_apps.jc.tower-research.com.txt
            replace fileserver1.jc:/n/fileserver1/home entry with anvil.jc.tower-research.com:/n/fileserver1/home
            git commit
            git push
            cfdeploy <site>
            """
        elif opt in ("-b", "--backout"):
            print "Doing a rollback. Please wait for few seconds\n"
            rollback()
            time.sleep(5)
        else:
            usage()
            sys.exit()


if __name__ == "__main__":

    if os.environ['USER'] != 'root':
        print "%s Script must be run by root user\n"
        sys.exit(1)

    # Todo: Check if the fileserver is actually down (use ping)


    #  main()
    # plumb_fs1_ip()

# Lv can be created before hand
# Create a symlink as ln -s /n/fileserver1/home  /n/systems1/homesnaps/hourly.0/fileserver1" + "." + domain

