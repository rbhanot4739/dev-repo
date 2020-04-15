from collections import OrderedDict
from time import time

import base64
import csv
import requests
import smtplib
from datetime import date as dt
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from fabric import Connection
from queue import Queue
from threading import Thread

from console_checker import serial_console_checker, SerialPasswordError, SerialError

host_info = {}
today = dt.today().strftime("%F")
parm = base64.b64decode(
    open('config.dat').read())


def get_hosts(q):
    """
    This function queries the rackdb api and returns the dictionary host_info
    with valid hostnames as key and Notes for each
    host as its value
    :return: host_info
    """
    global host_info
    portal_url = ""
    while not q.empty():
        site = q.get()
        host_and_site = ('{}.*{}'.format('install', site))

        query_string = [(
            'format',
            'json',
        ), ('username', ''),
            ('api_key',
             ''),
            ('limit', "500"), ('hostname__iregex', host_and_site)]

        query = OrderedDict(query_string)
        resp = requests.get(portal_url, params=query)
        resp.raise_for_status()
        data = resp.json()
        hosts_queue = Queue()
        for obj in data['objects']:
            if 'lab' not in obj['hostname']:
                hosts_queue.put(obj)
        ths = []
        for _ in range(hosts_queue.qsize()):
            t = Thread(target=threaded_console_checker, args=(hosts_queue,))
            t.start()
            ths.append(t)

        for t in ths:
            t.join()


def threaded_console_checker(q):
    global parm
    global host_info
    while not q.empty():
        obj = q.get()
        host = obj['hostname']
        site = obj['hostname'].split('.')[-1]
        notes = obj['notes'] if obj['notes'] else '    '

        try:
            total_reboots = list(reversed(Connection(host).run("last -xF|awk '/boot/{print $6 $9}'",
                                                               hide=True).stdout.strip().splitlines()))
            if len(total_reboots) > 5:
                last_reboot = total_reboots.pop()
                if total_reboots.count(last_reboot) > 5:
                    host_info[host] = site + '~' + notes + '~Unstable host with multiple reboots'
                    # print(host, 'multi')
        except Exception as e:
            try:
                serial_console_checker(host, parm)
                host_info[host] = site + '~' + notes + '~Console Okay, No Network'
                # print(host, 'un')
            except (SerialPasswordError, SerialError):
                host_info[host] = site + '~' + notes + '~No Console, No Network'
                # print(host, 'dead')


def make_host_dict():
    threads = []
    sites = ('')
    q = Queue()
    for i in sites:
        q.put(i)

    for _ in range(len(sites)):
        thread = Thread(target=get_hosts, args=(q,))
        thread.start()
        threads.append(thread)

    for th in threads:
        th.join()


def make_csv():
    global host_info
    global today
    with open('' + today + '.csv',
              'w') as outputCsvFile:
        csv_writer = csv.writer(
            outputCsvFile, delimiter=",", quotechar='"', quoting=csv.QUOTE_ALL)
        csv_writer.writerow(['Hostname', 'Site', 'State', 'Notes'])

        for k, v in sorted(host_info.items(), key=lambda x: x[1]):
            site, notes, state, = v.split('~')
            csv_writer.writerow([k, site, state, notes])


def send_mail():
    global today
    """
    Sends the email with generated csv as attachment
    :return:
    """

    # Email the generated csv file
    from_add = ''
    to_add = ['']
    # to_add = ['']
    cc_add = [']

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
    recipients = to_add + cc_add
    server = smtplib.SMTP('localhost')
    server.sendmail(from_add, recipients, message)
    server.quit()


start = time()
make_host_dict()
make_csv()
send_mail()

print(time() - start)
