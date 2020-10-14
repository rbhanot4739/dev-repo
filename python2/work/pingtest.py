#!/usr/bin/python3

import subprocess
import requests
import csv
import smtplib
from collections import OrderedDict
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from datetime import date as dt

today = dt.today().strftime("%F")


def get_hosts():
    """
    This function queries the rackdb api and returns the dictionary host_info with valid hostnames as key and Notes for each
    host as its value
    :return: host_info
    """
    portal_url = "https://portal.tower-research.com/portal/api/v1/"
    rack_db_mapping = "mapping"
    host_info = dict()
    sites = ()

    for site in sites:
        host_and_site = ('{}.*{}'.format('install', site)).replace('%', '.*')

        query_string = [('format', 'json',), ('username', ''),
                        ('api_key', ''), ('limit', "500"),
                        ('hostname__iregex', host_and_site)]

        query = OrderedDict(query_string)
        resp = requests.get(portal_url + rack_db_mapping, params=query)
        resp.raise_for_status()
        data = resp.json()

        for obj in data['objects']:
            host_info[obj['hostname']] = obj['notes']

    return host_info


def get_unreachable_hosts():
    """
    creates the csv file for the hosts which are not reachable
    :return: None
    """
    hosts = get_hosts()
    with open('/apps/nttech/rbhanot/ping-reports/' + today + '.csv', 'w', newline='') as outputCsvFile:
        csv_writer = csv.writer(
            outputCsvFile, delimiter=",", quotechar='"', quoting=csv.QUOTE_ALL)
        csv_writer.writerow(['Hostname', 'Notes'])

        for host in hosts:
            ping = subprocess.check_output(
                ['/usr/bin/which', 'fping']).decode().strip('\n')
            try:
                subprocess.check_call(
                    [ping, '-C', '1', '-q', host], stderr=subprocess.PIPE)
            except subprocess.CalledProcessError as e:
                csv_writer.writerow([host, hosts[host]])


def send_mail():
    """
    Sends the email with generated csv as attachment
    :return:
    """
    get_unreachable_hosts()

    # Email the generated csv file
    from_add = 'rbhanot@'
    to_add = ['']
    # to_add = ['rbhanot@']
    cc_add = ['rbhanot@']

    msg = MIMEMultipart()
    msg['From'] = from_add
    msg['To'] = ','.join(to_add)
    msg['Cc'] = ','.join(cc_add)
    msg['Subject'] = 'Unreachable Install Boxes on ' + today
    body = """Hello,
        
    Please find the attached csv file for the unreachable install boxes for {}.
    
    Thanks,
    Rohit Bhanot    
    """.format(today)

    # Attach the email body to MIMEMultipart object
    msg.attach(MIMEText(body, 'plain'))

    filename = 'Unreachable_Intsall_servers-' + today + '.csv'.format(today)

    # Attach the file to the email
    with open('/apps/nttech/rbhanot/ping-reports/' + today + '.csv', 'rb') as attachment:
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


if __name__ == "__main__":
    send_mail()
