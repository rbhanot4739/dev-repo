#!/usr/bin/python3.5

import os

print("Content-type: text/html\r\n\r\n")
print("<font size=+1>Environment</font><\br>")
for var in os.environ:
    print("{} = {}".format(var, os.environ[var]))
