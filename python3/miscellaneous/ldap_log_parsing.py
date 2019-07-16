# Author: Rohit Bhanot
# Date: Dec 21-2016
# Purpose: Parse LDAP(OpenDJ) logs to give Bind and Search operations statstics.

# !/usr/bin/python
import os, re, sys, datetime, time
from collections import defaultdict
from memory_profiler import *


@profile()
def main():
    start_time = datetime.datetime.now()
    _bindConn = defaultdict(str)
    _bindCount = defaultdict(int)
    _searchCount = defaultdict(int)
    _searchconn = defaultdict(int)
    today = datetime.date.today()
    date_delta = today.replace(day=1) - datetime.timedelta(days=1)
    date_range = (today - datetime.timedelta(days=4)).strftime("%Y%m%d")

    # if len(sys.argv) == 2:
    #         if (sys.argv[1]).lower() == 'm':
    #                 date_range = str(date_delta.year)+str(date_delta.month)
    #         elif (sys.argv[1]).lower() == 'd':
    #                 date_range = (today-datetime.timedelta(days=4)).strftime("%Y%m%d")
    #         else:
    #                 print("Only M/m and 'D/d are acceptable arguments")
    #                 exit(1)
    # else:
    #         print("Invalid number of arguments !!\nPlease pass M/m for parsing the logs for Last Month OR D/d for parsing Last Day logs.")
    #         exit(1)

    accessLogPath = "C:\\Rohit\\ECD Utilization Script - Copy\\logdir"
    statisticsLogFile = "C:\\Rohit\\ECD Utilization Script - Copy\\stats" + date_range + ".txt"

    _totalSearches = 0
    _totalBinds = 0
    _fname_patt = re.compile(r'access\.' + date_range + '.*')

    for file in re.findall(_fname_patt, '\n'.join(os.listdir(accessLogPath))):
        IN = open(accessLogPath + file)
        for line in IN:
            reg1 = re.search(r' BIND REQ .*conn=(\d+).*dn=(.*")', line)
            reg2 = re.search(r' SEARCH REQ .*conn=(\d+).*', line)
            if reg1:
                _totalBinds += 1
                uid, con = reg1.group(2, 1)
                uid = uid.lower()
                _bindCount[uid] = _bindCount[uid] + 1
                _bindConn[con] = uid

            if reg2:
                _totalSearches += 1
                skey = reg2.group(1)
                _searchconn[skey] += 1
        IN.close()
    for conid in _searchconn:
        if conid in _bindConn:
            new_key = _bindConn[conid]
            _searchCount[new_key] = _searchCount[new_key] + _searchconn[conid]

    _bindCount = sorted(_bindCount.items(), key=lambda i: i[1], reverse=True)[:20]
    _searchCount = sorted(_searchCount.items(), key=lambda i: i[1], reverse=True)[:20]

    OUT = open(statisticsLogFile, "w")
    OUT.writelines("\nTotal no of Bind Operations = " + str(_totalBinds) + "\n\n")

    for k, v in _bindCount:
        OUT.writelines(str(k) + " = " + str(v) + "\n")  # print(k," = ",v)

    OUT.writelines("\n**********************************************************************************\n")
    OUT.writelines("\nTotal no of Search Operations made today =" + str(_totalSearches) + "\n\n")
    OUT.writelines("\nNumber of Search Operations made by applications that Binded today \n\n")

    for k, v in _searchCount:
        OUT.writelines(k + " = " + str(v) + "\n")  # print(k," = ",v)

    time_taken = datetime.datetime.now() - start_time
    OUT.writelines("\nScript ran on " + str(time.ctime()) + "\nTotal time taken : " + str(time_taken) + "\n")

    OUT.close()


if __name__ == "__main__":
    main()
    print("Total memory usage : {}".format(memory_usage()))
