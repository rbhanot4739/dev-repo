#!/usr/bin/python

# Author: Rohit Bhanot
# Date:  Nov 15, 2018

from __future__ import print_function

import sys

import MySQLdb as mysql
import psycopg2
import re
import subprocess as sb
from collections import defaultdict
from functools import partial
from getpass import getpass, getuser
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT


def format_list_users(params=None, func=None):
    if func is None:
        return partial(format_list_users, params)

    def wrapper(obj):
        print('+' * 133)
        print('| %-15s | %-50s | %-42s | %-13s |' % getattr(obj, params))
        print('+' * 133)
        users = func(obj)
        for usr in users:
            for host, val in users[usr].items():
                print("| %-15s | %-50s | %-42s | %-13s |" % (
                    usr, host, val[0], val[1]))
        print('+' * 133)
        return users

    return wrapper


def limit_non_root_user(param=None, func=None):
    if func is None:
        return partial(limit_non_root_user, param)

    def wrapper(*args, **kwargs):
        if logged_user != 'root':
            if 'privileges' not in func.__name__:
                print(
                    "\nThis operation can only be performed by database super "
                    "user !!")
                return
            else:
                if getattr(args[0], param) == 'n':
                    print("\nDirect privilege operation not permitted to "
                          "non-root user !!\n")
                else:
                    func(*args, **kwargs)
        else:
            func(*args, **kwargs)

    return wrapper


class Base(object):
    _fields = ('host', 'port', 'user', 'password', 'dbtype')

    def __init__(self, *args):
        if len(args) != len(self.__class__._fields):
            raise TypeError("Invalid no of args passed !")
        for name, val in zip(self.__class__._fields, args):
            setattr(self, name, val)
        try:
            if args[-1] == 'postgres':
                self.conn = psycopg2.connect(host=self.host, port=self.port,
                                             user=self.user,
                                             password=self.password)
                self.conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
            elif args[-1] == 'mysql':
                self.conn = mysql.connect(host=self.host, port=self.port,
                                          user=self.user, passwd=self.password)
            else:
                pass

            self.cursor = self.conn.cursor()
        except Exception as e:
            print('\n', e)
            sys.exit("!! Error: Failed to connect to database !!\n")

    def manage_databases(self):
        db_tasks = {'l': self.list_databases, 'c': self.create_database,
                    'd': self.drop_database, 'u': self.update_db_owner,
                    'q': lambda: sys.exit()}
        ans = raw_input("\nChoose a database operation to do [l(list), "
                        "c(create), d(drop), u(update db owner(only for "
                        "postgresql)), q(go back)]: ").lower()
        while ans != 'q':
            db_tasks.get(ans, lambda: "")()
            ans = raw_input("\nChoose a database operation to do [l(list), "
                            "c(create), d(drop), u(update db owner(only for "
                            "postgresql)), q(go back)]: ").lower()

    def list_databases(self):
        print("+----------------------+")
        print("| Database             |")
        print("+----------------------+")
        for row in self.cursor.fetchall():
            print("%s %-20s %s" % ("|", row[0], "|"))
        print("+----------------------+")

    @staticmethod
    def create_database():
        db_name = raw_input("\nEnter the database name: ")
        if db_name is '':
            print("\nDatabase name not provided !!!")
            return
        elif not re.match("^[a-zA-Z0-9_]*$", db_name):
            print("Invalid characters found in database name !!!\n")
            return
        else:
            return db_name

    @limit_non_root_user()
    def drop_database(self):
        ans = raw_input("\nTHIS IS A HIGHLY DESTRUCTIVE OPERATION, ARE YOU "
                        "REALLY SURE YOU WANT TO DO THIS (y/n)? : ")
        if ans.lower() == 'y':
            db_name = raw_input("\nEnter database name to be dropped: ")
            if db_name is '':
                print("\nDatabase name not provided !!!")
                return
            try:
                self.cursor.execute("drop database %s;" % db_name)
                print('\n!!! Database "%s" dropped successfully !!!' % db_name)
            except Exception as e:
                print("\n%s !!" % str(e).strip('\n'))
            return
        else:
            return

    @limit_non_root_user()
    def update_db_owner(self):
        ans = raw_input("\nARE YOU SURE YOU WANT TO CHANGE THE DB OWNER(y/n) "
                        "?: ").lower()
        if ans == 'y':
            db_name = raw_input("Enter the database: ")
            db_owner = raw_input("Enter the new db owner name: ")
            try:
                self.cursor.execute(
                    "alter database %s owner to %s;" % (db_name, db_owner))
                print("\n!!! Owner for %s changed to %s successfully !!!" % (
                    db_name, db_owner))
            except Exception as e:
                print('\n', str(e).strip('\n'))
                return
        else:
            return

    def manage_users(self):
        usr_tasks = {'l': self.list_users, 'c': self.create_user,
                     'd': self.drop_user, 'u': self.update_user, }
        ans = raw_input(
            "\nChoose a user operation to do [l(list), c(create), d("
            "delete), u(set/update password), q(go back)]: "
            "").lower()
        while ans != 'q':
            usr_tasks.get(ans, lambda: "")()
            ans = raw_input(
                "\nChoose a user operation to do [l(list), c(create),"
                " d(delete), u(set/update password), q(go back)]: ")

    def build_user_list(self):
        users = defaultdict(dict)
        for f1, f2, f3, f4 in self.cursor.fetchall():
            users[f1].update({f2: (f3, f4)})
        return users

    @staticmethod
    def get_user_details():
        u_name = raw_input("\nEnter the username: ")
        _pass1 = getpass("Enter the password: ")
        _pass2 = getpass("Confirm the password: ")
        while _pass1 != _pass2:
            print("\n!! Passwords do not match !!\n")
            _pass1 = getpass("Enter the password: ")
            _pass2 = getpass("Confirm the password: ")
        return u_name, _pass1

    _user_list_fields = ()

    @format_list_users(params='_user_list_fields')
    def list_users(self):
        try:
            return self.build_user_list()
        except mysql.OperationalError as e:
            sys.exit(e)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        print("\nClosing the database connection...\n")
        self.conn.close()


class Postgres(Base):
    def __init__(self, *args):
        super(Postgres, self).__init__(*args)

    def list_databases(self):
        self.cursor.execute("Select datname from pg_database;")
        super(Postgres, self).list_databases()

    def create_database(self):
        db_name = super(Postgres, self).create_database()
        db_owner = raw_input("Enter the database owner name: ")
        if db_owner == '':
            print("\nDatabase Owner is mandatory !!")
            return
        try:
            self.cursor.execute(
                "create database %s with owner %s;" % (db_name, db_owner))
            print('\n!! Database "%s" created successfully with owner as '
                  '"%s" !!' % (db_name, db_owner))
        except Exception as e:
            print('\n', str(e).strip('\n'))

    def build_user_list(self):
        self.cursor.execute("select rolname,rolsuper,rolcreaterole,rolcreatedb"
                            " from pg_catalog.pg_roles;")
        return super(Postgres, self).build_user_list()

    _user_list_fields = (
        'User', 'RoleSuperUser', 'RoleCreateRole', 'RoleCreateDB')

    def create_user(self):
        u_name, u_pass = super(Postgres, self).get_user_details()
        try:
            self.cursor.execute(
                "create user %s with password '%s'" % (u_name, u_pass))
            print("\n!!! User %s created successfully !!!\n" % u_name)
            self.build_user_list()
            ans = raw_input("Do you want to assign roles as well to newly "
                            "created user y/n ?: ").lower()
            if ans == 'y':
                self.through_create = 'y'
                self.manage_privileges(u_name=u_name, resp='a')
                self.through_create = 'n'
            return
        except Exception as e:
            print('\n', str(e).strip('\n'))
            return

    @limit_non_root_user()
    def drop_user(self):
        u_name = raw_input("\nEnter the user name: ")
        try:
            self.cursor.execute("drop user %s;" % u_name)
            print("\n!!! User %s dropped successfully !!!\n" % u_name)
            self.build_user_list()
        except Exception as e:
            print(str(e).strip('\n'))
            return

    @limit_non_root_user()
    def update_user(self):
        u_name, u_pass = super(Postgres, self).get_user_details()
        try:
            self.cursor.execute(
                "alter user %s with password '%s';" % (u_name, u_pass))
            print(
                "\n!!! Password updated successfully for user %s !!!\n" % u_name)
        except psycopg2.ProgrammingError as e:
            print('\n', str(e).strip('\n'))
            return

    through_create = 'n'

    @limit_non_root_user(param='through_create')
    def manage_privileges(self, u_name=None, resp=None):

        print("\nExisting roles for users\n")
        self.list_users()
        if u_name is None:
            u_name = raw_input("\nEnter the username you manage roles for: ")
        try:
            roles = {'d': 'createdb', 'r': 'createrole',
                     'b': 'createdb,createrole'}
            if resp is None:
                resp = raw_input(
                    "Do you want to add(a)/remove(r) roles ?: ").lower()
            ans = raw_input("Choose the roles you want to update ["
                            "craeterole(r), createdb(d), "
                            "both(b)] : ").lower()
            if resp == 'a':
                for r in roles[ans].split(','):
                    self.cursor.execute("alter role %s with %s" % (u_name, r))
                print("\n !!! Roles added successfully !!!")
            elif resp == 'r':
                for r in roles[ans].split(','):
                    self.cursor.execute(
                        "alter role %s with no%s" % (u_name, r))
                print("\n !!! Roles removed successfully !!!")
            else:
                print("Wrong input provided !!")
                return
        except Exception as e:
            print('\n', str(e).strip('\n'))
            return


class Mysql(Base):
    def __init__(self, *args):
        super(Mysql, self).__init__(*args)

    def list_databases(self):
        self.cursor.execute("show databases;")
        super(Mysql, self).list_databases()

    def create_database(self):
        db_name = super(Mysql, self).create_database()
        try:
            self.cursor.execute("create database %s ;" % db_name)
            print('\n!!! Database "%s" created successfully !!!' % db_name)
        except mysql.ProgrammingError as e:
            print("\n%s !!" % e[1])
            return

    @limit_non_root_user()
    def update_db_owner(self):
        print("\nThe script does not support this operation for Mysql "
              "currently !!")
        return

    def build_user_list(self):
        self.cursor.execute('select user,host,password,super_priv  from '
                            'mysql.user;')
        return super(Mysql, self).build_user_list()

    _user_list_fields = ('User', 'Hostname', 'Password', 'SuperUserPriv')

    def create_user(self):
        users = self.build_user_list()
        u_name, u_pass = super(Mysql, self).get_user_details()
        # u_name = raw_input("\nEnter the username: ")

        resp = raw_input("\nDo you want to enable only localhost access or "
                         "only remote access or both"
                         ", choose [l/r/b]: ").lower()

        if resp == 'l':
            hosts = 'localhost'
        elif resp == 'r' or resp == 'b':
            ans = raw_input("Enter comma separated host string without any"
                            " spaces/or just type % for all hosts: ")
            if resp == 'r':
                hosts = ans
            else:
                hosts = ans + ',localhost'
        else:
            return "Invalid option !!!"

        hosts = [i.strip(' ') for i in hosts.split(',') if
                 i not in users[u_name].keys()]
        if len(hosts) == 0:
            print('\nUser already exists with mentioned hostname in the '
                  'database !!!\n')
            return
        # u_pass = raw_input("Enter the password to set for user: ")
        try:
            for host_string in hosts:
                self.cursor.execute(
                    "create user '%s'@'%s' identified by '%s';" % (
                        u_name, host_string, u_pass))
            print("\n!!! User %s created successfully !!!\n" % u_name)
            self.build_user_list()
            response = raw_input("Do you want to grant privileges to newly "
                                 "created user y/n ?: ")
            if response.lower() == 'y':
                self.through_create = 'y'
                self.manage_privileges(priv_mode='grant', u_name=u_name,
                                       ans='y')
                self.through_create = 'n'
            return
        except mysql.OperationalError as e:
            print(e)
            return

    @limit_non_root_user()
    def drop_user(self):
        users = self.build_user_list()
        u_name = raw_input("\nEnter username you want to delete: ")
        if u_name not in users:
            print("\nUser does not exists in the database !!!\n")
            return
        resp = raw_input("\nDo you want to remove user from localhost or "
                         "remote hosts or both, choose[l/r/b]: ").lower()
        if resp == 'l':
            hosts = ['localhost']
        elif resp == 'r':
            hosts = [i for i in users[u_name].keys() if i != 'localhost']
        elif resp == 'b':
            hosts = users[u_name].keys()
        else:
            return "Invalid option !!!"

        try:
            for host_string in hosts:
                self.cursor.execute(
                    "drop user '%s'@'%s';" % (u_name, host_string))

            self.cursor.execute("flush privileges;")
            print("\n!!! User %s dropped successfully !!!" % u_name)
            self.build_user_list()
        except mysql.OperationalError as e:
            print(e)
            return

    @limit_non_root_user()
    def update_user(self):
        users = self.build_user_list()
        u_name, u_pass = super(Mysql, self).get_user_details()
        # u_name = raw_input("Enter the user name: ")
        # u_pass = raw_input("Enter the password you want to set: ")
        if u_name not in users:
            print("\nUser does not exists in the database !!!\n")
            return
        try:
            self.cursor.execute("update mysql.user set password=password('%s')"
                                " where user='%s';" % (u_pass, u_name))
            print(
                "\n!!! Password updated successfully for user %s !!!\n" % u_name)
            self.build_user_list()

        except mysql.OperationalError as e:
            print(e)

    through_create = 'n'

    @limit_non_root_user(param='through_create')
    def manage_privileges(self, priv_mode=None, u_name=None, ans=None):
        users = self.list_users()
        if u_name is None:
            u_name = raw_input("\nEnter username to list the privileges: ")
        print("\nShowing exiting privileges for %s\n" % u_name)
        for host in users[u_name].keys():
            self.cursor.execute("show grants for '%s'@'%s'" % (u_name, host))
            for row in self.cursor.fetchall():
                print(row)
        if ans is None:
            ans = raw_input("\nDo you update privileges y/n ?: ").lower()
        if ans == 'y':
            if priv_mode is None:
                priv_mode = raw_input("Grant(g) or Revoke(r): ").lower()
            if priv_mode == 'g' or priv_mode == 'grant':
                priv_mode = 'grant'
                adjective = 'to'
            elif priv_mode == 'r':
                priv_mode = 'revoke'
                adjective = 'from'
            else:
                print("Wrong input only g/r are allowed, Exiting")
                return

            db_name = raw_input(
                "\nEnter database name you want to manage privileges on: ")

            resp = raw_input("Read-only(r) or Read-write(rw): ")
            priv_name = 'all' if resp == 'rw' else 'select'
            if priv_mode == 'grant' and priv_name == 'all' and (
                    db_name == '*' or db_name == 'mysql'):
                print("\nOnly root user can have write privileges on *.* and "
                      "mysql "
                      "!!!\n")
                return
            try:
                for host in users[u_name].keys():
                    self.cursor.execute("%s %s on %s.* %s '%s'@'%s';" % (
                        priv_mode, priv_name, db_name, adjective, u_name,
                        host))

                print('\n!!! %s was successful !!!\n' % priv_mode.capitalize())
            except mysql.OperationalError as e:
                print(e)
        else:
            return


def main():
    global logged_user

    if logged_user != 'root':
        print("Script must be run by root user")  # sys.exit(1)

    host = 'localhost'
    password = getpass("Enter password for root user: ")

    def show_mysql_running_instances():
        ports = sb.Popen("ps -ef | grep mysql | grep -E -o 'port=+[0-9]+' |"
                         "sort -u", stdout=sb.PIPE, stderr=sb.PIPE,
                         shell=True).communicate()[0].splitlines()

        if ports:
            print("Multiple instances of mysql found running on following "
                  "ports.")
            print('\n'.join(ports))
            dport = raw_input("Enter the port you want to connect on")
        else:
            dport = 3306
        return dport

    def menu():
        print()
        print("%s MAIN MENU %s" % ('*' * 10, '*' * 10))
        print("1: Manage Databases")
        print("2: Manage Users")
        print("3: Manage Privileges")
        print("q: Quit")
        print("*" * 31, "\n")

    dbtype = raw_input(
        "Which DB you want to work on Mysql(m)/Postgres(p): ").lower()
    if dbtype == 'm':
        user = 'root'
        port = show_mysql_running_instances()
        db_type = 'mysql'
        Database = Mysql
    elif dbtype == 'p':
        user = 'postgres'
        port = 5432
        db_type = 'postgres'
        Database = Postgres
    else:
        sys.exit('\nWrong option , Exiting \n!!')

    with Database(host, port, user, password, db_type) as db:
        choices = {'1': db.manage_databases, '2': db.manage_users,
                   '3': db.manage_privileges, 'q': lambda: sys.exit("User "
                                                                    "exited")}
        menu()
        resp = raw_input("Press a key: ")
        while resp:
            choices.get(resp, lambda: "")()
            menu()
            resp = raw_input("Press a key: ")


if __name__ == "__main__":
    try:
        logged_user = getuser()
        main()
    except KeyboardInterrupt:
        sys.exit("\nCtrl-c issued by user !!!")

# todo Add entry to pg_hba.conf for new db/user - as this controls which
# user can connect to what database
