#!/usr/bin/python2
#
# Fetch key performance data to send to graphite for analysis
#

# heretofore maintained by myeun :(
# (setq python-indent-guess-indent-offset nil)
# (setq python-indent-offset 4)

# Updates/Revisions

# 22/01/2018: Rohit Bhanot : Added the functions get_huge_pages() at line 640
# and get_non_root_rt_processes() at line 661. Function calls at 839 and 842

import platform
import socket
import time
import sys
import os
import os.path
import fcntl
import subprocess
import re
import traceback
import shutil
import glob
from collections import defaultdict
from multiprocessing import cpu_count

CARBON_SERVER = 'graphite-dev.tower-research.com'
CARBON_SERVER1 = 'systemsdb1.newark.tower-research.com'
CARBON_PORT = 2003

# Default time to sleep in daemon (-d mode)
# Can be changed with -d N, where N is the number of seconds to sleep
TIME_TO_SLEEP = 60

LOCK_FILE = "/tmp/.server_stats.lock"


class CpuStat:
    def __init__(self, name, user, nice, sys, idle, iowait, irq, softirq):
        self.name = name
        self.user = int(user)
        self.nice = int(nice)
        self.system = int(sys)
        self.idle = int(idle)
        self.iowait = int(iowait)
        self.irq = int(irq)
        self.softirq = int(softirq)
        self.total = int(user) + int(nice) + int(sys) + int(idle) + int(iowait)

    def user():
        return self.user

    def total():
        return self.total

    def nice():
        return self.nice

    def system():
        return self.system

    def idle():
        return self.idle

    def iowait():
        return self.iowait

    def irq():
        return self.irq

    def softirq():
        return self.softirq

    def __str__(self):
        return "Cpustat for %s : user %s nice %s system %s idle %s iowait %s irq %s softirq %s" % (
            self.name, self.user, self.nice, self.system, self.idle, self.iowait, self.irq, self.softirq)


def get_loadavgs():
    with open('/proc/loadavg') as f:
        return f.read().strip().split()[:3]


def get_uptime():
    with open('/proc/uptime') as f:
        return round(float(f.read().strip().split()[0]) / 3600 / 24, 1)


def get_default_interface():
    """Read the default interface directly from /proc."""
    with open("/proc/net/route") as fh:
        for line in fh:
            fields = line.strip().split()
            if fields[1] != '00000000' or not int(fields[3], 16) & 2:
                continue
            return fields[0]


def get_netstats():
    defaultInterface = get_default_interface()
    with open('/proc/net/dev') as f:
        for line in iter(f.readline, ''):
            # sometimes overflow pushes the first number against the colon -- force space after colon
            tokens = line.strip().replace(":", ": ").split()
            if tokens[0].startswith(defaultInterface):
                return tokens


# todo: same stats for Lookups
#   Lookups n=N Number of lookup calls made on cache backends
#        neg=N   Number of negative lookups made
#        pos=N   Number of positive lookups made
#        crt=N   Number of objects created by lookup
#        tmo=N   Number of lookups timed out and requeued
# https://github.com/torvalds/linux/blob/master/Documentation/filesystems/caching/backend-api.txt
# https://github.com/torvalds/linux/blob/master/Documentation/filesystems/caching/fscache.txt
def get_fscachestats():
    last = {}
    current = {}
    diff = {}
    lastfile = '/dev/shm/.fscachestats'
    currentfile = '/proc/fs/fscache/stats'

    try:
        linelist = list()
        with open(lastfile) as f:
            for line in iter(f.readline, ''):
                if line.startswith('Retrvls'):
                    m = re.findall(r'(\S+)=(\d+)', line)
                    linelist.extend(m)
        last = dict(linelist)

        linelist = list()
        with open(currentfile) as f:
            for line in iter(f.readline, ''):
                if line.startswith('Retrvls'):
                    m = re.findall(r'(\S+)=(\d+)', line)
                    linelist.extend(m)
        current = dict(linelist)

        for k in current.keys():
            diff[k] = int(current[k]) - int(last[k])

        # avoid div by zero
        if diff['n'] == 0:
            diff['hitrate'] = 0
        else:
            diff['hitrate'] = round(100.0 * diff['ok'] / diff['n'], 2)

        if diff['n'] == 0:
            diff['errrate'] = 0
        else:
            diff['errrate'] = round(
                100.0 * (diff['nbf'] + diff['int'] + diff['oom']) / diff['n'], 2)

        return diff

    except Exception, e:
        return None

    finally:
        shutil.copy(currentfile, lastfile)


def get_diskspace():
    fs_types = ['ext4', 'xfs']
    ignore_mounts = [' / ', ' /tmp ', ' /var ', ' /boot ']
    diskspace = []
    diskspace1 = []
    with open('/etc/mtab') as f:
        for line in iter(f.readline, ''):
            if any(fstype in line for fstype in fs_types):
                if not any(mount in line for mount in ignore_mounts):
                    words = line.split(' ')
                    path = words[1]
                    disk = os.statvfs(path)
                    # totalBytes = round(float(disk.f_bsize*disk.f_blocks) / 1024 / 1024 / 1024, 2)
                    totalAvailSpace = round(
                        float(disk.f_bsize * disk.f_bavail) / 1024 / 1024 / 1024, 2)
                    totalUsedSpace = round(
                        float(disk.f_bsize * (disk.f_blocks - disk.f_bfree)) / 1024 / 1024 / 1024, 2)
                    totalBytes = round(
                        float((totalAvailSpace + totalUsedSpace)), 2)
                    if [words[0], totalBytes, totalUsedSpace, totalAvailSpace] not in diskspace:
                        diskspace.append(
                            [words[0], totalBytes, totalUsedSpace, totalAvailSpace])
                        path = words[1].replace('/', '_')
                        if path[0] == '_':
                            path = path[1:]
                        diskspace1.append(
                            [path, totalBytes, totalUsedSpace, totalAvailSpace])
    return diskspace1


def calc_netstats():
    prevstats = get_netstats()
    time.sleep(1)
    newstats = get_netstats()

    r_Mbps = ((float(newstats[1]) - float(prevstats[1])) * 8) / (1024 * 1024)
    t_Mbps = ((float(newstats[9]) - float(prevstats[9])) * 8) / (1024 * 1024)
    return [prevstats[0].rstrip(":"), r_Mbps, t_Mbps]


def get_memstats():
    memstat = {}
    with open('/proc/meminfo') as f:
        for line in iter(f.readline, ''):
            fields = line.strip().split()
            memstat[fields[0].rstrip(':')] = fields[1]
    return memstat


def get_fpgatemp():
    fpga_logfile = "/spare/scratch/fpga_temp.log"
    fpga_temps = {}
    if os.path.isfile(fpga_logfile):
        with open(fpga_logfile) as f:
            for line in f:
                fields = []
                line = line.strip()
                fields = line.split()
                numf = len(fields)
                temp = int(fields[numf - 3])
                dev = []
                for i in range(1, numf - 4):
                    dev.append(fields[i])
                fpga_dev = str(dev).strip('[]')
                fpga_dev = re.sub('\'|,', '', fpga_dev)
                fpga_dev = re.sub('\s+', '_', fpga_dev)
                fpga_temps[fpga_dev] = temp
        return fpga_temps


def get_cpustats():
    cpustat = {}
    with open('/proc/stat') as f:
        for line in iter(f.readline, ''):
            fields = line.strip().split()
            if fields[0].startswith('cpu'):
                cpu = CpuStat(fields[0], fields[1], fields[2], fields[3],
                              fields[4], fields[5], fields[6], fields[7])
                cpustat[fields[0]] = cpu
    return cpustat


def get_cpustats_summary():
    cpustat = {}
    procs_running = 0
    procs_blocked = 0
    with open('/proc/stat') as f:
        for line in iter(f.readline, ''):
            fields = line.strip().split()
            if fields[0] == 'cpu':
                cpu = CpuStat(fields[0], fields[1], fields[2], fields[3],
                              fields[4], fields[5], fields[6], fields[7])
                cpustat[fields[0]] = cpu
            if fields[0] == 'procs_running':
                procs_running = fields[1]
            if fields[0] == 'procs_blocked':
                procs_blocked = fields[1]
    return cpustat, procs_running, procs_blocked


def get_vmstats():
    vmstat = {'pgrefill': 0, 'pgsteal': 0, 'pgsteal_kswapd': 0, 'pgsteal_direct': 0, 'pgscan': 0, 'pgscan_kswapd': 0,
              'pgscan_direct': 0, }
    currentfile = '/proc/vmstat'

    with open(currentfile) as f:
        for line in iter(f.readline, ''):
            fields = line.strip().split()
            if len(fields) < 2:
                continue
            m = re.search(
                '^(pg(?:scan|steal|refill))(_(?:kswapd|direct))?', fields[0])
            if m:
                vmstat[m.group(1)] += int(fields[1])
                if m.group(2):
                    vmstat[m.group(1) + m.group(2)] += int(fields[1])
            elif re.search('^(pageoutrun|allocstall|pswp)', fields[0]):
                vmstat[fields[0]] = int(fields[1])
    return vmstat


def get_mailqstats():
    maildir = "/var/spool/mqueue"
    try:
        qlength = len([name for name in os.listdir(maildir)
                       if os.path.isfile(os.path.join(maildir, name))])
    except OSError, e:
        return None
    return qlength


def get_temperatures():
    temps = {}
    filler = ""

    # bail out early if path doesn't exist
    if not os.path.exists('/sys/class/hwmon/'):
        print
        "/sys/class/hwmon missing, skipping temps"
        return temps

    for d in os.listdir('/sys/class/hwmon/'):
        try:
            name = open('/sys/class/hwmon/%s/name' % d).readlines()[0].rstrip()
        except:
            try:
                name = open('/sys/class/hwmon/%s/device/name' %
                            d).readlines()[0].rstrip()
                filler = "/device"
            except:
                name = "unknown"

        # try:
        if 1 == 1:
            name = name.replace(' ', '_')
            temps[name] = {}
            old = None
            tmp = {}
            for t in sorted(os.listdir('/sys/class/hwmon/%s/%s' % (d, filler))):
                if t.startswith('temp'):
                    if 'alarm' in t:
                        pass
                    current = t.split('_')[0]
                    if old is None:
                        old = current
                    if current != old:
                        temps[name][old] = tmp
                        old = current
                        tmp = {}

                    if 'crit' in t:
                        tmp[t] = open('/sys/class/hwmon/%s/%s/%s' %
                                      (d, filler, t)).readlines()[0].rstrip()
                        tmp[t] = int(tmp[t])
                    if 'label' in t:
                        tmp[t] = open('/sys/class/hwmon/%s/%s/%s' %
                                      (d, filler, t)).readlines()[0].rstrip()
                        tmp[t] = tmp[t].replace(' ', '_')
                    if 'input' in t:
                        tmp[t] = open('/sys/class/hwmon/%s/%s/%s' %
                                      (d, filler, t)).readlines()[0].rstrip()
                        tmp[t] = int(tmp[t])  # except IOError, e:  #    pass

    return temps


def get_ifacestats():
    try:
        ret = {}
        for line in open('/proc/net/dev').readlines():
            if 'Inter' in line or 'face' in line or 'lo:' in line:
                # then we have the header, or the loopback
                continue
            # we have a genuine interface
            iface, rest = line.split(':')
            iface = iface.strip()
            rest = rest.strip()
            (rx_bytes, rx_packets, rx_errs, rx_drop, rx_fifo, rx_frame, rx_compressed, rx_multicast, tx_bytes,
             tx_packets, tx_errs, tx_drop, tx_fifo, tx_frame, tx_compressed, tx_multicast) = rest.split()

            ret[iface] = {'rx_bytes': rx_bytes, 'rx_packets': rx_packets, 'rx_errs': rx_errs, 'rx_drops': rx_drop,
                          'rx_fifo': rx_fifo, 'rx_frame': rx_frame, 'rx_compressed ': rx_compressed, 'rx_multicast': rx_multicast,
                          'tx_bytes': tx_bytes, 'tx_packets': tx_packets, 'tx_errs': tx_errs, 'tx_drops': tx_drop,
                          'tx_fifo': tx_fifo, 'tx_frame': tx_frame, 'tx_compressed ': tx_compressed,
                          'tx_multicast': tx_multicast, }

            ethtool = '/sbin/ethtool'
            p = subprocess.Popen(
                [ethtool, '-i', iface], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
            lines = p.stdout.readlines()
            if len(lines) < 1 or not re.match('driver\s*:\s*sfc', lines[0]):
                continue

            p = subprocess.Popen(
                [ethtool, '-S', iface], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
            for line in p.stdout.readlines():
                if not re.search('(trunc|discard)_vfifo', line):
                    continue
                words = line.split(':')
                if len(words) != 2:
                    continue
                stat = words[0].strip()
                value = words[1].strip()
                ret[iface][stat] = value

        return ret
    except Exception, e:
        # no interfaces ?
        traceback.print_exc()
        return None


# iostat method - NOT USED - we use the diskstats method below
def get_diskstats_iostat():
    stats = {}
    p = subprocess.Popen(['iostat', '-k', '-d', '-x', '-y', '1', '1'],
                         stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    for line in p.stdout.readlines():
        if line.startswith('Linux') or line.startswith('Device') or '.' not in line:
            continue
        (dev, rrqm, wrqm, read, write, rkbs, wkbs,
         avgrq, avgqu, await, svctm, util) = line.split()
        stats.setdefault(dev, {})
        stats[dev]['rrqm'] = rrqm
        stats[dev]['wrqm'] = wrqm
        stats[dev]['read'] = read
        stats[dev]['write'] = write
        stats[dev]['rkbs'] = rkbs
        stats[dev]['wkbs'] = wkbs
        stats[dev]['avgrq'] = avgrq
        stats[dev]['avgqu'] = avgqu
        stats[dev]['await'] = await
        stats[dev]['svctm'] = svctm
        stats[dev]['util'] = util

    return stats


# for now, in the interest of reducing the number of metrics,
# log data only for fscache and spare block devices
# todo: send all current raw data
def get_diskstats():
    currentfile = '/proc/diskstats'
    lastfile = '/dev/shm/.diskstatscache'

    # device used by spare
    sparedev = os.readlink('/dev/mapper/vg_root-lv_spare')
    sparedev = re.split('/', sparedev)[1]

    # device used by fscache
    fscachedev = ''
    with open('/proc/mounts') as f:
        for line in iter(f.readline, ''):
            m = re.match(r'/dev/(sd\S+)\s+/var/cache/fscache', line)
            if m:
                fscachedev = m.group(1)

    try:
        last = {}
        ret = {}
        timestamp = time.time()
        timediff = (timestamp - os.stat(lastfile).st_ctime)
        for line in open(lastfile).readlines():
            (major, minor, dev, reads, rmerges, rsectors, rtime, writes, wmerges, wsectors, wtime, current, iotime,
             wetime) = line.split()
            if dev == fscachedev:
                dev = 'fscachedev'
            elif dev == sparedev:
                dev = 'sparedev'
            else:
                continue

            last.setdefault(dev, {})
            last[dev]['reads'] = int(reads)
            last[dev]['rmerges'] = int(rmerges)
            last[dev]['rsectors'] = int(rsectors)
            last[dev]['rtime'] = int(rtime)
            last[dev]['writes'] = int(writes)
            last[dev]['wmerges'] = int(wmerges)
            last[dev]['wsectors'] = int(wsectors)
            last[dev]['wtime'] = int(wtime)
            last[dev]['current'] = int(current)
            last[dev]['time'] = int(iotime)
            last[dev]['wetime'] = int(wetime)

        for line in open(currentfile).readlines():
            (major, minor, dev, reads, rmerges, rsectors, rtime, writes, wmerges, wsectors, wtime, current, iotime,
             wetime) = line.split()
            if dev == fscachedev:
                dev = 'fscachedev'
            elif dev == sparedev:
                dev = 'sparedev'
            else:
                continue

            ret.setdefault(dev, {})
            ret[dev]['reads'] = int(reads) - last[dev]['reads']
            ret[dev]['rmerges'] = int(rmerges) - last[dev]['rmerges']
            ret[dev]['rsectors'] = int(rsectors) - last[dev]['rsectors']
            ret[dev]['rtime'] = int(rtime) - last[dev]['rtime']
            ret[dev]['writes'] = int(writes) - last[dev]['writes']
            ret[dev]['wmerges'] = int(wmerges) - last[dev]['wmerges']
            ret[dev]['wsectors'] = int(wsectors) - last[dev]['wsectors']
            ret[dev]['wtime'] = int(wtime) - last[dev]['wtime']
            # current is not monotonically increasing
            ret[dev]['current'] = int(current)
            ret[dev]['time'] = int(iotime) - last[dev]['time']
            ret[dev]['wetime'] = int(wetime) - last[dev]['wetime']

            # this is equivalent to iostat's utilization, read, write, r_await, w_await
            # let's ignore div by zero; a few missing metrics is fine, and this
            # rarely occurs
            ret[dev]['util'] = round(ret[dev]['time'] / timediff / 10, 2)
            ret[dev]['weutil'] = round(ret[dev]['wetime'] / timediff / 10, 2)
            ret[dev]['rmb'] = round(
                ret[dev]['rsectors'] * 512 / 1024 / 1024 / timediff, 2)
            ret[dev]['wmb'] = round(
                ret[dev]['wsectors'] * 512 / 1024 / 1024 / timediff, 2)
            ret[dev]['rawait'] = round(
                1.0 * ret[dev]['rtime'] / ret[dev]['reads'], 2) if ret[dev]['reads'] else 0.0
            ret[dev]['wawait'] = round(
                1.0 * ret[dev]['wtime'] / ret[dev]['writes'], 2) if ret[dev]['writes'] else 0.0

            # time is in jiffies = 100 us, not ms
        #           ret[dev]['rawtime'] = int(time) / 10.0
        # 512b sectors, so divide by 2 for kb
        #           ret[dev]['rawrkb'] = int(rsectors) / 2.0
        #           ret[dev]['rawwkb'] = int(wsectors) / 2.0

        return ret

    except Exception, e:
        traceback.print_exc()
        return None

    finally:
        shutil.copy(currentfile, lastfile)


def get_condor_exec_stats():
    stats = {}
    stats['cpus'] = 0
    stats['childcpus'] = 0
    stats['totalcpus'] = 0
    stats['memory'] = 0
    stats['childmemory'] = 0
    stats['totalmemory'] = 0
    stats['totalpss'] = 0
    stats['freememory'] = 0
    fqdn = platform.node()

    cmdargs = ['condor_status', '-const', 'PartitionableSlot', '-direct', fqdn, '-af', 'Cpus', 'sum(ChildCpus)',
               'TotalCpus', 'Memory', 'sum(ChildMemory)', 'TotalMemory', 'TotalPSS']
    p = subprocess.Popen(cmdargs, stdout=subprocess.PIPE,
                         stderr=subprocess.PIPE)

    try:
        for line in p.stdout:
            line = line.rstrip()
            cpus, childcpus, totalcpus, memory, childmemory, totalmemory, totalpss = line.split()
            stats['cpus'] = int(cpus)
            stats['childcpus'] = int(
                childcpus) if childcpus != 'undefined' else 0
            stats['totalcpus'] = int(float(totalcpus))
            stats['memory'] = int(memory)
            stats['childmemory'] = int(
                childmemory) if childmemory != 'undefined' else 0
            stats['totalmemory'] = int(totalmemory)
            stats['totalpss'] = int(totalpss)
            stats['freememory'] = stats['totalmemory'] - stats['totalpss']
            if stats['cpus'] == 0:
                stats['freememorypercpu'] = stats['freememory']
            else:
                stats['freememorypercpu'] = stats['freememory'] / stats['cpus']
            return stats
    except:
        return None


def get_condor_schedd_stats():
    # TODO: run this only on the master, use python bindings
    stats = {}
    stats['running'] = 0
    stats['idle'] = 0
    stats['held'] = 0
    stats['removed'] = 0
    stats['completed'] = 0
    fqdn = platform.node()

    # contact the local schedd directly;
    # all values will be 0 if no schedd is running
    cmdargs = ['condor_status', '-schedd', '-direct', fqdn, '-af', 'TotalRunningJobs', 'TotalIdleJobs', 'TotalHeldJobs',
               'TotalRemovedJobs', 'JobsCompleted']
    p = subprocess.Popen(cmdargs, stdout=subprocess.PIPE,
                         stderr=subprocess.PIPE)

    try:
        for line in p.stdout:
            line = line.rstrip()
            running, idle, held, removed, completed = line.split()
            stats['running'] = int(running)
            stats['idle'] = int(idle)
            stats['held'] = int(held)
            stats['removed'] = int(removed)
            stats['completed'] = int(completed)
    except:
        return None

    # Avoid needlessly returning stats on non-submit hosts
    if sum(stats.values()) == 0:
        return None
    else:
        return stats


def get_ptp_offset():
    ptp_log = None
    for daemon in ('ptpd2', 'sfptpd2'):
        if subprocess.call("pgrep -x " + daemon + " >/dev/null", shell=True) == 0:
            if daemon == 'ptpd2':
                ptp_log = '/var/log/ptpd2.stats'
                count = 60
                nelem = 6
            else:
                ptp_log = '/var/log/sfptpd.stats'
                count = 120
                nelem = 5
            break
    if not ptp_log:
        return None, None

    cmd = 'tail -' + str(count) + ' ' + ptp_log
    cat = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)
    pat = re.compile('\d{4}-\d{2}-\d{2}')
    sep = re.compile('[\s,]+')
    gm_off = None
    offsets = []

    while True:
        line = cat.stdout.readline()
        if not line:
            break
        if not pat.match(line):
            continue
        a = sep.split(line)
        if len(a) < nelem:
            gm_off = None
            continue
        if daemon == 'ptpd2':
            offsets.append(float(a[5]) * 1000000)
            continue
        if re.search('ptp-gm.*phc', line):
            gm_off = float(a[4])
            continue
        if not gm_off:
            continue
        if re.search('phc.*phc', line):
            continue
        if re.search('phc.*system', line):
            offsets.append((gm_off + float(a[4])) / 1000)
        gm_off = None
    l = len(offsets)
    if l == 0:
        return None, None
    offsets.sort()
    i = l / 2
    if l & 1:
        offset = offsets[i]
    else:
        offset = (offsets[i - 1] + offsets[i]) / 2
    if abs(offsets[0]) < abs(offsets[l - 1]):
        offset_max = offsets[l - 1]
    else:
        offset_max = offsets[0]
    return offset, offset_max


def get_huge_pages():
    """
    This function reports the total number of huge pages and the number of used huge pages
    """
    h_pages = dict()
    files = (f for f in glob.iglob(
        "/sys/devices/system/node/node*/hugepages/*/*") if "nr_" in f or "free_" in f)

    for FILE in files:
        fields = FILE.split('/')
        size = re.sub('[-a-zA-Z]', '', fields[-2])
        if int(size) / 1024 == 1024:
            p_size = '1G'
        elif int(size) / 1024 == 2.0:
            p_size = '2M'
        else:
            p_size = str(int(size) / 1024) + ' kB'

        key = fields[-4] + '.' + p_size + '.' + fields[-1]

        with open(FILE) as IF:
            h_pages[key] = IF.read().strip()

    return h_pages


def get_non_root_rt_processes():
    """
    Below function reports Real time process run by non-root users
    ps -eLo user,pid,tid,class,rtprio,ni,pri,psr,pcpu,stat,comm|awk '$1 != "root" && $4 != "-" {print $0}'
    :return: dictionary with psr number as key and total processes on that core as value
    """
    ps = ['ps', '-eLo', 'user,pid,tid,class,rtprio,ni,pri,psr,pcpu,stat,comm']
    awk = ['awk', '$1 != "root" && $5 != "-" {print $8}']
    total_processes = subprocess.Popen(ps, stdout=subprocess.PIPE)
    non_root_processes = subprocess.Popen(
        awk, stdin=total_processes.stdout, stdout=subprocess.PIPE)
    total_processes.stdout.close()
    procs_per_core = defaultdict(int)
    # remove the first header line from the output
    for line in non_root_processes.stdout:
        break

    for line in non_root_processes.stdout:
        procs_per_core[line.strip()] += 1
    non_root_processes.stdout.close()
    return procs_per_core


def send_msg(message):
    print 'sending message:\n%s' % message
    sock = socket.socket()
    sock.connect((CARBON_SERVER, CARBON_PORT))
    sock.sendall(message)
    sock.close()


def do_stats():
    node = platform.node().rsplit('.')[0]
    domain = platform.node().rsplit('.')[1]
    timestamp = int(time.time())

    loadavgs = get_loadavgs()
    uptime = get_uptime()
    netstats = calc_netstats()
    memstats = get_memstats()
    temp = get_temperatures()
    ifacestats = get_ifacestats()
    vmstats = get_vmstats()
    fpga_temp = get_fpgatemp()
    diskspace = get_diskspace()

    huge_pages = get_huge_pages()
    procs_per_core = get_non_root_rt_processes()

    if isPublicCondorExecNode or isPrivateCondorExecNode:
        condorstats = get_condor_exec_stats()
    elif isCondorScheddNode:
        condorstats = get_condor_schedd_stats()
    else:
        condorstats = None

    if isPublicCondorExecNode:
        cpustats, procs_running, procs_blocked = get_cpustats_summary()
        diskstats = get_diskstats()
        fscachestats = get_fscachestats()
        mailq = None
        default_iface = get_default_interface()

        # remove all but the default interface, and rename that to 'eth'
        for iface in ifacestats.keys():
            if not iface == default_iface:
                del ifacestats[iface]
        ifacestats['eth'] = ifacestats[default_iface]
        del ifacestats[default_iface]

    else:
        cpustats = get_cpustats()
        diskstats = None
        fscachestats = None
        mailq = get_mailqstats()

    mystats = ['MemTotal', 'MemFree', 'Buffers',
               'Cached', 'Active', 'SwapTotal', 'SwapFree']
    myifacestats = ['rx_bytes', 'rx_packets', 'rx_errs', 'rx_drops', 'rx_fifo', 'rx_frame', 'rx_compressed ',
                    'rx_multicast', 'rx_pm_trunc_vfifo_full', 'rx_pm_discard_vfifo_full', 'tx_bytes', 'tx_packets',
                    'tx_errs', 'tx_drops', 'tx_fifo', 'tx_frame', 'tx_compressed ', 'tx_multicast']

    lines = ['server.%s.%s.loadavg_1min %s %d' % (domain, node, loadavgs[0], timestamp),
             'server.%s.%s.loadavg_5min %s %d' % (
                 domain, node, loadavgs[1], timestamp),
             'server.%s.%s.loadavg_15min %s %d' % (
                 domain, node, loadavgs[2], timestamp),
             'server.%s.%s.net_%s_read_mbps %s %d' % (
                 domain, node, netstats[0], netstats[1], timestamp),
             'server.%s.%s.net_%s_write_mbps %s %d' % (domain, node, netstats[0], netstats[2], timestamp), ]

    if fscachestats is not None:
        for k, v in fscachestats.items():
            lines.append('server.%s.%s.fscache.%s %s %d' %
                         (domain, node, k, v, timestamp))

    if vmstats:
        for k, v in vmstats.items():
            lines.append('server.%s.%s.vmstat.%s %s %d' %
                         (domain, node, k, v, timestamp))

    if fpga_temp:
        for k, v in fpga_temp.items():
            lines.append('server.%s.%s.fpga_temp.%s %s %d' %
                         (domain, node, k, v, timestamp))

    if diskstats:
        for dev in diskstats:
            if dev.startswith('dm'):
                continue
            for stat in (
                'reads', 'rmerges', 'rsectors', 'rtime', 'writes', 'wmerges', 'wsectors', 'wtime', 'current', 'time',
                    'wetime', 'util', 'weutil', 'rmb', 'wmb', 'rawait', 'wawait'):
                lines.append(
                    'server.%s.%s.block.%s.%s %s %d' % (domain, node, dev, stat, diskstats[dev][stat], timestamp))

            # enable or disable in get_diskstats as needed
            try:
                for stat in ('rawtime', 'rawrkb', 'rawwkb'):
                    lines.append(
                        'server.%s.%s.block.%s.%s %s %d' % (domain, node, dev, stat, diskstats[dev][stat], timestamp))
            except:
                pass

    if condorstats:
        for stat in condorstats:
            lines.append('server.%s.%s.condor.%s %s %d' %
                         (domain, node, stat, condorstats[stat], timestamp))

    if mailq is not None:
        lines.append('server.%s.%s.mailq_length %s %d' %
                     (domain, node, mailq, timestamp))

    for stat in mystats:
        lines.append('server.%s.%s.%s_MB %s %d' % (
            domain, node, stat, float(memstats[stat]) / 1024, timestamp))

    for volume in diskspace:
        lines.append('server.%s.%s.fs.%s.Total_GB %s %d' %
                     (domain, node, volume[0], volume[1], timestamp))
        lines.append('server.%s.%s.fs.%s.Used_GB %s %d' %
                     (domain, node, volume[0], volume[2], timestamp))
        lines.append('server.%s.%s.fs.%s.Available_GB %s %d' %
                     (domain, node, volume[0], volume[3], timestamp))

    for cpu in cpustats:
        lines.append('server.%s.%s.%s.user %s %d' %
                     (domain, node, cpu, cpustats[cpu].user, timestamp))
        lines.append('server.%s.%s.%s.nice %s %d' %
                     (domain, node, cpu, cpustats[cpu].nice, timestamp))
        lines.append('server.%s.%s.%s.system %s %d' %
                     (domain, node, cpu, cpustats[cpu].system, timestamp))
        lines.append('server.%s.%s.%s.idle %s %d' %
                     (domain, node, cpu, cpustats[cpu].idle, timestamp))
        lines.append('server.%s.%s.%s.iowait %s %d' %
                     (domain, node, cpu, cpustats[cpu].iowait, timestamp))
        lines.append('server.%s.%s.%s.irq %s %d' %
                     (domain, node, cpu, cpustats[cpu].irq, timestamp))
        lines.append('server.%s.%s.%s.softirq %s %d' %
                     (domain, node, cpu, cpustats[cpu].softirq, timestamp))

    try:
        lines.append('server.%s.%s.procs_running %s %d' %
                     (domain, node, procs_running, timestamp))
        lines.append('server.%s.%s.procs_blocked %s %d' %
                     (domain, node, procs_blocked, timestamp))
    except:
        pass

    for component in temp.keys():
        for tempzone in temp[component].keys():
            for key in temp[component][tempzone].keys():
                value = temp[component][tempzone][key]
                the_key = key.replace("%s_" % tempzone, '')
                lines.append(
                    'server.%s.%s.temp.%s.%s.%s %s %d' % (domain, node, component, tempzone, the_key, value, timestamp))

    for iface in ifacestats.keys():
        for stat in myifacestats:
            if stat not in ifacestats[iface]:
                continue
            value = ifacestats[iface][stat]
            lines.append('server.%s.%s.iface.%s.%s %s %d' %
                         (domain, node, iface, stat, value, timestamp))

    ptp_offset, ptp_offset_max = get_ptp_offset()
    if ptp_offset is not None:
        lines.append('server.%s.%s.ptp_offset_us %.3f %d' %
                     (domain, node, ptp_offset, timestamp))
    if ptp_offset_max is not None:
        lines.append('server.%s.%s.ptp_offset_max_us %.3f %d' %
                     (domain, node, ptp_offset_max, timestamp))

    if uptime:
        lines.append('server.%s.%s.uptime %.1f %d' %
                     (domain, node, uptime, timestamp))

    for key in sorted(huge_pages, reverse=True):
        lines.append('server.%s.%s.hugepages.%s %s %d' %
                     (domain, node, key, huge_pages[key], timestamp))

    for core in range(cpu_count()):
        lines.append('server.%s.%s.rtProcesses.core%s %s %d' % (
            domain, node, core, procs_per_core.get(str(core), 0), timestamp))

    message = '\n'.join(lines) + '\n'
    try:
        send_msg(message)
    except Exception, e:
        print
        "%s: FAILED to send message to %s:%s; %s" % (
            timestamp, CARBON_SERVER, CARBON_PORT, str(e))


if __name__ == '__main__':
    # ensure same cpu affinity as the kernel (0 is the default)
    cpunum = 0
    try:
        twr_cpu = open("/proc/sys/kernel/tower_kernel_cpu")
        cpunum = twr_cpu.read()
        cpunum = int(cpunum)
    except:
        # if no file, or parse error, we fall back to 0
        pass
    os.system("taskset -pc %d %d" % (cpunum, os.getpid()))

    try:
        debug = sys.argv[1]
    except:
        debug = ''

    # get lock early
    f = open(LOCK_FILE, "w")
    try:
        fcntl.flock(f, fcntl.LOCK_EX | fcntl.LOCK_NB)
        if debug == '-d':
            print
            "locked"
    except:
        sys.stderr.write("unable to get lock on %s\n" % LOCK_FILE)
        sys.exit(1)

    me = socket.gethostname()
    # We don't care about install boxes
    if me.startswith('install'):
        sys.exit()

    isPrivateCondorExecNode = False
    isPublicCondorExecNode = False
    isCondorScheddNode = False

    if re.match('(ares|condor|hades|htd|htdst)(node|test)', me):
        isPublicCondorExecNode = True
    else:
        with open(os.devnull) as devnull:
            ec = subprocess.call(['/usr/bin/pgrep', '-u', 'condor', '-x', 'condor_startd'], stdout=devnull,
                                 stderr=devnull)
            if ec == 0:
                isPrivateCondorExecNode = True

    with open(os.devnull) as devnull:
        ec = subprocess.call(['/usr/bin/pgrep', '-u', 'condor',
                              '-x', 'condor_schedd'], stdout=devnull, stderr=devnull)
        if ec == 0:
            isCondorScheddNode = True

    try:
        sleeptime = int(sys.argv[2])
    except:
        sleeptime = TIME_TO_SLEEP

    try:
        if debug == '-d':
            while True:
                do_stats()
                time.sleep(sleeptime)
        else:
            do_stats()
    except Exception, e:
        traceback.print_exc()
    finally:
        # Remove lock file
        f.close()
        if os.path.isfile(LOCK_FILE):
            os.remove(LOCK_FILE)
