#!/usr/bin/env python

# Author: Rohit Bhanot
# Purpose: Check status of install machines

import base64
import csv
import multiprocessing
import Queue
import smtplib
import sys
import threading
import time
from collections import OrderedDict
from datetime import date as dt
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

import requests
from fabric.api import *

from console_checker import serial_console_checker


def get_hosts(q):
    """
    This function queries the rackdb api and returns the dictionary host_info
    with valid hostnames as key and Notes for each
    host as its value
    :return: host_info
    """
    global host_info
    portal_url = "https://portal.tower-research.com/portal/api/v1/mapping"
    while not q.empty():
        site = q.get()
        host_and_site = ('{}.*{}'.format('install', site))

        query_string = [(
            'format',
            'json',
        ), ('username', 'sysinfo-api'),
                        ('api_key',
                         '1a41b5c74aaea7bfa81aefc028fc83ec6e69f12d'),
                        ('limit', "500"), ('hostname__iregex', host_and_site)]

        query = OrderedDict(query_string)
        resp = requests.get(portal_url, params=query)
        resp.raise_for_status()
        data = resp.json()

        for obj in data['objects']:
            if 'lab' not in obj['hostname']:
                host = obj['hostname']
                site = obj['hostname'].split('.')[-1]
                notes = obj['notes'] if obj['notes'] else '    '
                host_info[host] = site + '~' + notes


def make_host_dict():
    threads = []
    sites = ('asx', 'busan-sf', 'gurg-dc', 'gurg-off', 'hk', 'hk-off', 'jnx',
             'jpn-maruya', 'jpx', 'jpx-sg', 'krx-kis', 'mumbai-bse',
             'mumbai-dakc', 'mumbai-nse', 'mumbai-off', 'mumbai-tata',
             'nebi-nse', 'nebi-tata', 'sgx', 'sing-off', 'syd-sy2', 'taifex',
             'tkp', 'tokyo-ty3')
    sites = ('sing-off',)
    q = Queue.Queue()
    for i in sites:
        q.put(i)

    for _ in range(25):
        thread = threading.Thread(target=get_hosts, args=(q, ))
        thread.start()
        threads.append(thread)

    for th in threads:
        th.join()


@task
@parallel(pool_size=25)
def runner():
    global host_info
    try:
        run('uptime')
        total_reboots = list(
            reversed(
                run("last -xF|awk '/boot/{print "
                    "$6 $9}'").splitlines()))
        if len(total_reboots) > 5:
            last_reboot = total_reboots.pop()
            if total_reboots.count(last_reboot) > 5:
                host_info[env.host] += '~Rebooting host'
                print('RR host {}'.format(env.host))
            else:
                del host_info[env.host]
        else:
            del host_info[env.host]
    except Exception as e:
        # print(e)
        console = serial_console_checker(str(env.host), param)
        # print(console, env.host)
        if console == 'Up':
            host_info[env.host] += '~Unreachable host'
            print('UN host {} '.format(env.host))
        if console == 'Down':
            host_info[env.host] += '~Dead host'
            print('Dead host {} '.format(env.host))


def make_csv():
    global host_info
    global today

    with open('/apps/nttech/rbhanot/installBox-reports/' + today + '.csv',
              'w') as outputCsvFile:
        csv_writer = csv.writer(
            outputCsvFile, delimiter=",", quotechar='"', quoting=csv.QUOTE_ALL)
        csv_writer.writerow(['Hostname', 'site', 'State', 'Notes'])

        for k, v in host_info.items():
            site, notes, state, = v.split('~')
            csv_writer.writerow([k, site, state, notes])


def send_mail():
    global today
    """
    Sends the email with generated csv as attachment
    :return:
    """

    # Email the generated csv file
    from_add = 'rbhanot@tower-research.com'
    to_add = ['seo-india@tower-research.com']
    # to_add = ['rbhanot@tower-research.com']
    cc_add = ['rbhanot@tower-research.com']

    msg = MIMEMultipart()
    msg['From'] = from_add
    msg['To'] = ','.join(to_add)
    msg['Cc'] = ','.join(cc_add)
    msg['Subject'] = 'Install Boxes report for ' + today
    body = """Hello,

    Please find the attached csv file for the unreachable install boxes for {}.

    Thanks,
    Rohit Bhanot
    """.format(today)

    # Attach the email body to MIMEMultipart object
    msg.attach(MIMEText(body, 'plain'))

    filename = 'Install_Box_Report_' + today + '.csv'.format(today)

    # Attach the file to the email
    with open('/apps/nttech/rbhanot/installBox-reports/' + today + '.csv',
              'rb') as attachment:
        part = MIMEBase('application', 'octet-stream')
        part.set_payload(attachment.read())
        encoders.encode_base64(part)
        part.add_header('Content-Disposition',
                        "attachment; filename= {}".format(filename))
    msg.attach(part)

    message = msg.as_string()
    recepieints = to_add + cc_add
    server = smtplib.SMTP('localhost')
    server.sendmail(from_add, recepieints, message)
    server.quit()


if __name__ == '__main__':
    try:
        s = time.time()
        param = base64.b64decode(
            open('/spare/ssd/rbhanot/nvim/share/nvim/'
                 'runtime/lua/.config/.config.dat').read())
        today = dt.today().strftime("%F")
        mp_manager = multiprocessing.Manager()
        host_info = mp_manager.dict()
        make_host_dict()

        env.hosts = host_info.keys()
        # env.hosts = ['install122.sing-off', ]

        with hide('everything'):
            execute(runner)

        make_csv()
        # send_mail()
        print(time.time() - s)
    except KeyboardInterrupt:
        sys.exit('Ctrl-c issued by user !!')
