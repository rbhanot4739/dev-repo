#!/bin/bash

read -p "Enter your username: " USER
echo "Enter your password"
read -s PASSWORD 

# for systems servers
for i in `get-cdp -_ systems1%|egrep -v "old|windows|repo|oob|systemsdb|hostname|gurg-off"`; do ./ssh-keys-from-remote.exp $i $USER $PASSWORD ; done
# for fw servers
#for i in `get-cdp -_ fw%`; do ./ssh-key-copy.exp $i $USER $PASSWORD ; done
