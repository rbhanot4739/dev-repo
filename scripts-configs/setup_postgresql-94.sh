#!/bin/bash

# Author: Rohit Bhanot
# Date: Nov 05, 2018
# Objective: This script setups the postgresql instance for the first time and updates the pg_hba.conf file appropriately.

CMD="
cat <<EOF > /etc/sysconfig/pgsql/postgresql-9.4
PGDATA=/spare/pgsql-9/9.4/data/
PGLOG=/spare/pgsql-9/9.4/pgstartup.log
EOF

/sbin/service postgresql-9.4 initdb

cp  /etc/fstab /spare/fstab.`date +%F%T`
mkdir /var/lib/pgsql
echo '/spare/pgsql-9    /var/lib/pgsql defaults,none   bind            0 0' >> /etc/fstab
mount /var/lib/pgsql

/sbin/service postgresql-9.4 start;

su - postgres <<EF
psql -d postgres -U postgres <<EOF
alter user postgres with encrypted password 'TowerMyDB';
create user nagios with encrypted password 'N@giosT0wer2016';
grant connect on database template1 to nagios;
EOF
EF

>/spare/pgsql-9/9.4/data/pg_hba.conf;

cat <<EOF > /spare/pgsql-9/9.4/data/pg_hba.conf
local   all             postgres                                peer
local   all             all                                     md5
host    all             postgres        127.0.0.1/32            md5
host    all             all             127.0.0.1/32            md5
host    template1       nagios          127.0.0.1/32            md5
EOF

sed -i \"s/^#listen_addresses = 'localhost'/listen_addresses = '*'/\" /spare/pgsql-9/9.4/data/postgresql.conf

/sbin/service postgresql-9.4 restart;
"

if [ `whoami` != "root" ]
then
	echo -e "\n !!! Script can only be run as root !!!\n"
	exit 1
fi


if [ $# == 0 ]
then
	echo -e "\n---------------------------------------------------------------------------------------------------------------------------" 
	echo -e "\nThe script will run the following sequence of commands."
	echo -e "Execute with '-r' option to actually run the script."
	echo -e "\n----------------------------------------------------------------------------------------------------------------------------" 
	echo "$CMD"
	echo -e "------------------------------------------------------------------------------------------------------------------------------" 

elif [[ $# == 1 && $1 == "-r" ]]
then
	service postgresql-9.4 status > /dev/null
	if [ $? == 0 ]
	then
		echo -e  "\npostgresql-9.4 is already running on this machine, Exiting !!!\n"
		exit 1
	fi

	if [ -d "/var/lib/pgsql/" -o -d "/spare/pgsql-9/" ]
	then
		echo -e "\nPostgres Data Directory exists on the server. Please check if /var/lib/pgsql/9.4/data/ OR /spare/pgsql-9 exists !!\n"
                echo -e "Confirm there is no running postgres instance and this is indeed first time setup. If yes then delete old Data Directory manually and run the script again !!\n"
		exit 1
	fi
	echo -e "\nSetting up ...........\n"
	eval "$CMD"
else
	echo "Please run the scrip with -r"
fi
