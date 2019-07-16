#!/bin/bash

# Author: Rohit Bhanot
# Date: Nov 05, 2018

CMD='
mkdir -p /spare/local/pgsql
cd /var/lib
ln -s /spare/local/pgsql pgsql
chown -h postgres:postgres /spare/local/pgsql/
chmod  700  /spare/local/pgsql/
su - postgres -c "/usr/pgsql-9.4/bin/initdb -D /var/lib/pgsql/9.4/data/";
/sbin/service postgresql-9.4 start;

psql -d postgres -U postgres <<EOF
alter user postgres with encrypted password "DBROOTPASSWD";
create user nagios with encrypted password "NAGIOSUSRPASSWD";
grant connect on database template1 to nagios;
EOF

>/var/lib/pgsql/9.4/data/pg_hba.conf;

cat <<EOF > /var/lib/pgsql/9.4/data/pg_hba.conf
local   all             postgres                                peer
local   all             all                                     md5
host    all             postgres        127.0.0.1/32            md5
host    all             all             127.0.0.1/32            md5
host    template1       nagios          127.0.0.1/32            md5
EOF

/sbin/service postgresql-9.4 restart;
'

if [ `whoami` != "root" ]
then
	echo -e "\n !!! Script can only be run as root !!!\n"
	exit 1
fi


if [ $# == 0 ]
then
	echo -e "\nThe script will run the following sequence of commands."
	echo -e "Execute with '-r' option to actually run the script."
	echo -e "\n--------------------------------------------------------------------" 
	echo "$CMD"
	echo -e "\n--------------------------------------------------------------------" 
elif [[ $# == 1 && $1 == "-r" ]]
then
	service postgresql-9.4 status > /dev/null
	if [ $? == 0 ]
	then
		echo -e  "\npostgresql-9.4 is already running on this machine, Exiting !!!\n"
		exit 1
	fi

	if [ -d "/var/lib/pgsql/9.4/data/" -o -d "/spare/local/pgsql" ]
	then
		echo -e "\nPostgres Data Directory exists on the server. Please check if /var/lib/pgsql/9.4/data/ OR /spare/local/pgsql/ exists !!\n"
echo -e "Confirm there is no running postgres instance and this is indeed first time setup. If yes then delete old Data Directory manually and run the script again !!\n"
		exit 1
	fi
	echo -e "\nSetting up ...........\n"
# /sbin/service postgresql-9.4 stop;
# killall -9 -u postgres

mkdir -p /spare/local/pgsql
cd /var/lib
if [ ! -e pgsql ]
then
	echo -e "\nCreating symlink for /var/lib/pgsql from /spare/local/pgsql\n"
	ln -s /spare/local/pgsql pgsql
fi
chown -h postgres:postgres /spare/local/pgsql/
chmod  700  /spare/local/pgsql/
su - postgres -c "/usr/pgsql-9.4/bin/initdb -D /var/lib/pgsql/9.4/data/";
/sbin/service postgresql-9.4 start;

psql -d postgres -U postgres <<EOF
alter user postgres with encrypted password 'TowerMyDB';
create user nagios with encrypted password 'N@giosT0wer2016';
grant connect on database template1 to nagios;
EOF

>/var/lib/pgsql/9.4/data/pg_hba.conf;

cat <<EOF > /var/lib/pgsql/9.4/data/pg_hba.conf
local   all             postgres                                peer
local   all             all                                     md5
host    all             postgres        127.0.0.1/32            md5
host    all             all             127.0.0.1/32            md5
host    template1       nagios          127.0.0.1/32            md5
EOF

/sbin/service postgresql-9.4 restart;
else
	echo "Please run the scrip with -r"
fi
