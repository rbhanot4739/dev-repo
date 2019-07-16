#!/usr/bin/python

# Author: Rohit Bhanot
# Date:  Nov 15, 2018

import sys
from collections import defaultdict

import MySQLdb as mysql
import psycopg2
import re
from fabric import Connection
from functools import partial
from getpass import getpass, getuser
from invoke.exceptions import UnexpectedExit
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT


def format_list_users(params=None, func=None):
    if func is None:
        return partial(format_list_users, params)

    def wrapper(obj):
        print('+' * 88)
        print('| %-15s | %-50s | %-13s |' % getattr(obj, params))
        print('+' * 88)
        users = func(obj)
        for usr, val in users.items():
            for k, v in val.items():
                print("| %-15s | %-50s | %-13s |" % (usr, k, v))
        print('+' * 88)
        return users

    return wrapper


def limit_non_root_user(param=None, func=None):
    if func is None:
        return partial(limit_non_root_user, param)

    def wrapper(*args, **kwargs):
        if logged_user != 'root':
            if 'privileges' or 'roles' in func.__name__:
                if getattr(args[0], param) == 'y':
                    func(*args, **kwargs)
                else:
                    print("\nDirect access management operation not permitted "
                          "to non-root user !!")
            else:
                print(
                    "\nThis operation can only be performed by database super "
                    "user !!")
                return
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
                self.conn = psycopg2.connect(
                    host=self.host,
                    port=self.port,
                    user=self.user,
                    password=self.password)
                self.conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
            elif args[-1] == 'mysql':
                self.conn = mysql.connect(
                    host=self.host,
                    port=self.port,
                    user=self.user,
                    passwd=self.password)
            else:
                pass

            self.cursor = self.conn.cursor()
        except Exception as e:
            print('\n', e)
            sys.exit("!! Error: Failed to connect to database !!\n")

    def manage_databases(self):
        db_tasks = {
            'l': self.list_databases,
            'c': self.create_database,
            'd': self.drop_database,
            'u': self.update_db_owner,
            'q': lambda: sys.exit()
        }
        ans = input("\nChoose a database operation to do [l(list), "
                    "c(create), d(drop), u(update db owner(only for "
                    "postgresql)), q(go back)]: ").lower()
        while ans != 'q':
            db_tasks.get(ans, lambda: "")()
            ans = input("\nChoose a database operation to do [l(list), "
                        "c(create), d(drop), u(update db owner(only for "
                        "postgresql)), q(go back)]: ").lower()

    def list_databases(self):
        return self.cursor.fetchall()

    def create_database(self):
        db_name = input("\nEnter the database name: ")
        if db_name is '' or not re.match("^[a-zA-Z0-9_]*$", db_name):
            print("\nDatabase name can't be blank and can only contain "
                  "characters [a-zA-Z0-9_] !!!")
            db_name = self.create_database()
        else:
            try:
                self.cursor.execute("create database %s" % (db_name))
                print('\n!! Database "%s" created successfully !!' % (db_name))
            except Exception as e:
                print('\n', str(e).strip('\n'))
            return db_name

    @limit_non_root_user()
    def drop_database(self):
        ans = input("\nTHIS IS A HIGHLY DESTRUCTIVE OPERATION, ARE YOU "
                    "REALLY SURE YOU WANT TO DO THIS (y/n)? : ")
        if ans.lower() == 'y':
            db_name = input("\nEnter database name to be dropped: ")
            if db_name is '':
                print("\nDatabase name not provided !!!")
                return
            if db_name in ('mysql', 'postgres', 'template0', 'template1'):
                print("\nDrop not permitted on %s" % db_name)
                return
            try:
                self.cursor.execute("drop database %s;" % db_name)
                print('\n!!! Database "%s" dropped successfully !!!' % db_name)
            except Exception as e:
                print("\n%s !!" % str(e).strip('\n'))
            return
        else:
            return

    @staticmethod
    def get_user_details():
        u_name = input("\nEnter the username: ")
        if u_name is '' or not re.match("^[a-zA-Z0-9_]*$", u_name):
            print("Username can't be blank and can only contain "
                  "characters [a-zA-Z0-9_] !!!")
            u_name = Base.get_user_details()
        _pass1 = getpass("Enter the password: ")
        _pass2 = getpass("Confirm the password: ")
        while _pass1 != _pass2:
            print("\n!! Passwords do not match !!\n")
            _pass1 = getpass("Enter the password: ")
            _pass2 = getpass("Confirm the password: ")
        return u_name, _pass1

    def manage_users(self):
        usr_tasks = {
            'l': self.list_users,
            'c': self.create_user,
            'd': self.drop_user,
            'u': self.update_user,
        }
        ans = input(
            "\nChoose a user operation to do [l(list), c(create), d("
            "delete), u(set/update password), q(go back)]: "
            "").lower()
        while ans != 'q':
            usr_tasks.get(ans, lambda: "")()
            ans = input(
                "\nChoose a user operation to do [l(list), c(create),"
                " d(delete), u(set/update password), q(go back)]: ")

    def build_user_list(self):
        users = defaultdict(dict)
        for f1, f2, f3 in self.cursor.fetchall():
            users[f1].update({f2: (f3)})
        return users

    _user_list_fields = ()

    @format_list_users(params='_user_list_fields')
    def list_users(self):
        try:
            return self.build_user_list()
        except mysql.OperationalError as e:
            sys.exit(e)

    def manage_access(self):
        _tasks = {
            'p': self.manage_privileges,
            'r': self.manage_roles,
            'q': lambda: sys.exit()
        }
        ans = input("\nChoose a operation to do [r(Manage Roles)"
                    ", p(Manage Privileges), q(Go Back) ").lower()
        while ans != 'q':
            _tasks.get(ans, lambda: "")()
            ans = input(
                "\nChoose a database operation to do [r(Manage Roles)"
                ", p(Manage Privileges), q(Go Back) ").lower()

    through_create = ''

    @limit_non_root_user(param='through_create')
    def manage_privileges(self, u_name=None, priv_mode=None):
        self.users = self.build_user_list()
        self.u_name = u_name
        self.priv_mode = priv_mode
        if self.u_name is None:
            print('+' * 17)
            for user in self.users:
                print('| %-13s |' % user)
            print('+' * 17)
            self.u_name = input("\nEnter username to update the "
                                "privileges for: ")
        self.db_names = input(
            "\nEnter comma separated list of database names you want to "
            "manage privileges on: ")
        if self.priv_mode is None:
            self.priv_mode = input("Grant(g) or Revoke(r): ").lower()
        if self.priv_mode == 'g':
            self.priv_mode = 'grant'
            self.adjective = 'to'
        elif self.priv_mode == 'r':
            self.priv_mode = 'revoke'
            self.adjective = 'from'
        else:
            print("Wrong input only g/r are allowed, Exiting")
            return

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        print("\nClosing the database connection...\n")
        self.cursor.close()
        self.conn.close()


class Postgres(Base):
    def __init__(self, *args):
        super(Postgres, self).__init__(*args)

    def list_databases(self):
        self.cursor.execute("Select datname from pg_database;")
        super(Postgres, self).list_databases()

    def create_database(self):
        db_name = super(Postgres, self).create_database()
        # Restrict privileges on newly created database
        self.cursor.execute("revoke all on database %s from public;" % db_name)
        # Revoke privileges on all schema public in the newly created database
        self.temp_conn = psycopg2.connect(
            host=self.host,
            port=self.port,
            user=self.user,
            password=self.password,
            database=db_name)
        self.temp_conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        c = self.temp_conn.cursor()
        c.execute("revoke all on schema public from public;")
        c.close()
        self.temp_conn.close()

    @limit_non_root_user()
    def update_db_owner(self):
        ans = input("\nARE YOU SURE YOU WANT TO CHANGE THE DB OWNER(y/n) "
                    "?: ").lower()
        if ans == 'y':
            db_name = input("Enter the database: ")
            db_owner = input("Enter the new db owner name: ")
            try:
                self.cursor.execute(
                    "alter database %s owner to %s;" % (db_name, db_owner))
                print("\n!!! Owner for %s changed to %s successfully !!!" %
                      (db_name, db_owner))
            except Exception as e:
                print('\n', str(e).strip('\n'))
                return
        else:
            return

    def build_user_list(self):
        self.cursor.execute("select rolname,rolcreaterole,rolcreatedb"
                            " from pg_catalog.pg_roles;")
        return super(Postgres, self).build_user_list()

    _user_list_fields = ('User', 'RoleCreateRole', 'RoleCreateDB')

    def create_user(self):
        u_name, u_pass = super(Postgres, self).get_user_details()
        try:
            self.cursor.execute(
                "create user %s with password '%s'" % (u_name, u_pass))
            print("\n!!! User %s created successfully !!!\n" % u_name)
            self.build_user_list()
            ans = input("Do you want to assign privileges as well to "
                        "newly created user y/n ?: ").lower()
            if ans == 'y':
                self.through_create = 'y'
                self.manage_privileges(u_name=u_name, priv_mode='g')
                self.through_create = 'n'
            return
        except Exception as e:
            print('\n', str(e).strip('\n'))
            return

    @limit_non_root_user()
    def drop_user(self):
        # TODO: Exception is being printed
        u_name = input("\nEnter the user name: ")
        if u_name in ('postgres', 'nagios'):
            print("\nNot allowed to delete `postgres` or `nagios` user !! ")
            return
        try:
            self.cursor.execute("drop user %s;" % u_name)
            print("\n!!! User %s dropped successfully !!!" % u_name)
        except Exception as e:
            if 'cannot be dropped because some objects depend on ' in str(e):
                db_names = set([
                    i.rpartition(' ')[-1]
                    for i in re.findall(r'database.*', str(e))
                ])
                resp = input(
                    '\nTHERE ARE OBJECTS OWNED BY THIS USER IN '
                    'DATABASES [%s], DO YOU REALLY WANT TO '
                    'DELETE THIS USER (y) ?: ' % ', '.join(db_names)).lower()
                if resp == 'y':
                    try:
                        for db in db_names:
                            self.temp_conn = psycopg2.connect(
                                host=self.host,
                                port=self.port,
                                user=self.user,
                                password=self.password,
                                database=db)
                            self.temp_conn.set_isolation_level(
                                ISOLATION_LEVEL_AUTOCOMMIT)
                            c = self.temp_conn.cursor()
                            c.execute("drop owned by %s" % u_name)
                            c.close()
                            self.temp_conn.close()
                        self.cursor.execute("drop role %s" % u_name)
                        print(
                            "\n!!! User %s dropped successfully !!!" % u_name)
                    except Exception as p:
                        print('\n %s !!' % str(p).strip('\n'))
                else:
                    print("\nDidn't get 'y' as response, Manually delete the "
                          "user from database !!")
                    return
            else:
                print('\n %s !!' % str(e).strip('\n'))

        self.build_user_list()

    @limit_non_root_user()
    def update_user(self):
        u_name, u_pass = super(Postgres, self).get_user_details()
        try:
            self.cursor.execute(
                "alter user %s with password '%s';" % (u_name, u_pass))
            print("\n!!! Password updated successfully for user %s !!!\n" %
                  u_name)
        except psycopg2.ProgrammingError as e:
            print('\n', str(e).strip('\n'))
            return

    through_create = 'n'

    @limit_non_root_user(param='through_create')
    def manage_privileges(self, u_name=None, priv_mode=None):
        super(Postgres, self).manage_privileges(u_name, priv_mode)
        try:

            for db_name in self.db_names.split(','):
                self.temp_conn = psycopg2.connect(
                    host=self.host,
                    port=self.port,
                    user=self.user,
                    password=self.password,
                    database=db_name)
                self.temp_conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
                c = self.temp_conn.cursor()

                c.execute("grant usage on schema public to %s;" % self.u_name)

                resp = input("\nRead-only(ro) or Read-write(rw) [%s]: " %
                             db_name).lower()
                if resp == 'ro':
                    self.cursor.execute(
                        "%s connect on database %s %s %s;" %
                        (self.priv_mode, db_name, self.adjective, self.u_name))
                    c.execute("%s select on all tables in schema public %s %s"
                              % (self.priv_mode, self.adjective, self.u_name))

                if resp == 'rw':
                    if db_name not in ('postgres', 'template0', 'template1'):
                        self.cursor.execute("%s all on database %s %s %s;" %
                                            (self.priv_mode, db_name,
                                             self.adjective, self.u_name))
                        c.execute(
                            "%s all on  schema public %s %s" %
                            (self.priv_mode, self.adjective, self.u_name))
                        ans = input("Since this is a RW user, do you "
                                    "want to assign some roles as well "
                                    "to this user (y/n)? : ").lower()
                        if ans == 'y':
                            self.through_privs = 'y'
                            self.manage_roles(u_name=u_name, type='a')
                            self.through_privs = 'n'
                    else:
                        print(
                            "Only SuperUser can have Read-Write privileges on "
                            "('postgres', 'template0', 'template1')")
                        return

                c.close()
                self.temp_conn.close()
                print("\n%s was successful on %s!!\n" %
                      (self.priv_mode.capitalize(), db_name))
        except Exception as e:
            print(e)

    through_privs = 'n'

    @limit_non_root_user(param='through_privs')
    def manage_roles(self, u_name=None, type=None):
        # TODO: Work to be done
        print("\nExisting roles for users\n")
        self.list_users()
        if u_name is None:
            u_name = input("\nEnter the username you manage roles for: ")
        try:
            roles = {
                'd': 'createdb',
                'r': 'createrole',
                'b': 'createdb,createrole'
            }
            if type is None:
                type = input(
                    "Do you want to add(a)/remove(r) roles ?: ").lower()
            ans = input("Choose the roles you want to update ["
                        "craeterole(r), createdb(d), "
                        "both(b)] : ").lower()
            if type == 'a':
                for r in roles[ans].split(','):
                    self.cursor.execute("alter role %s with %s" % (u_name, r))
                print("\n !!! Roles added successfully !!!")
            elif type == 'r':
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
        return super(Mysql, self).list_databases()

    def create_database(self):
        super(Mysql, self).create_database()

    @limit_non_root_user()
    def update_db_owner(self):
        print("\nThe script does not support this operation for Mysql "
              "currently !!")
        return

    def build_user_list(self):
        self.cursor.execute('select user,host,super_priv  from ' 'mysql.user;')
        return super(Mysql, self).build_user_list()

    _user_list_fields = ('User', 'Hostname', 'SuperUserPriv')

    def create_user(self):
        users = self.build_user_list()
        u_name, u_pass = super(Mysql, self).get_user_details()
        # u_name = input("\nEnter the username: ")

        resp = input("\nDo you want to enable only localhost access or "
                     "only remote access or both"
                     ", choose [l/r/b]: ").lower()

        if resp == 'l':
            hosts = 'localhost'
        elif resp == 'r' or resp == 'b':
            ans = input("Enter comma separated host string without any"
                        " spaces/or just type % for all hosts: ")
            if resp == 'r':
                hosts = ans
            else:
                hosts = ans + ',localhost'
        else:
            return "Invalid option !!!"

        hosts = [
            i.strip(' ') for i in hosts.split(',')
            if i not in users[u_name].keys()
        ]
        if len(hosts) == 0:
            print('\nUser already exists with mentioned hostname in the '
                  'database !!!\n')
            return
        # u_pass = input("Enter the password to set for user: ")
        try:
            for host_string in hosts:
                self.cursor.execute("create user '%s'@'%s' identified by '%s';"
                                    % (u_name, host_string, u_pass))
            print("\n!!! User %s created successfully !!!\n" % u_name)
            self.build_user_list()
            response = input("Do you want to grant privileges to newly "
                             "created user y/n ?: ")
            if response.lower() == 'y':
                self.through_create = 'y'
                self.manage_privileges(u_name=u_name, priv_mode='g')
                self.through_create = 'n'
            return
        except mysql.OperationalError as e:
            print(e)
            return

    @limit_non_root_user()
    def drop_user(self):
        users = self.build_user_list()
        u_name = input("\nEnter username you want to delete: ")
        if u_name == 'root':
            print("\nNot allowed to delete `root` user !! ")
            return
        if u_name not in users:
            print("\nUser does not exists in the database !!!\n")
            return
        resp = input("\nDo you want to remove user from localhost or "
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
        if u_name not in users:
            print("\nUser does not exists in the database !!!\n")
            return
        try:
            self.cursor.execute("update mysql.user set password=password('%s')"
                                " where user='%s';" % (u_pass, u_name))
            print("\n!!! Password updated successfully for user %s !!!\n" %
                  u_name)
            self.build_user_list()

        except mysql.OperationalError as e:
            print(e)

    through_create = 'n'

    @limit_non_root_user(param='through_create')
    def manage_privileges(self, u_name=None, priv_mode=None):
        super(Mysql, self).manage_privileges(u_name, priv_mode)
        for db_name in self.db_names.split(','):
            resp = input(
                "Read-only(ro) or Read-write(rw) [%s]: " % db_name)
            priv_name = 'all' if resp == 'rw' else 'select'
            if self.priv_mode == 'g' and priv_name == 'all' and (
                    db_name == '*' or db_name == 'mysql'):
                print("\nOnly root user can have write privileges on *.* and "
                      "mysql !!!\n")
                return
            try:
                for host in self.users[self.u_name].keys():
                    self.cursor.execute("%s %s on %s.* %s '%s'@'%s';" %
                                        (self.priv_mode, priv_name, db_name,
                                         self.adjective, self.u_name, host))

                print('\n!!! %s was successful on %s!!!\n' %
                      (self.priv_mode.capitalize(), db_name))
            except mysql.OperationalError as e:
                print(e)

    @limit_non_root_user()
    def manage_roles(self):
        print("\nThis is not a Mysql feature.")
        return


def show_mysql_running_instances(host, logged_user, pwd, dbtype):
    try:
        result = Connection(host, logged_user, connect_kwargs={"password": pwd}).run(
            "ps -ef | grep \[m\]ysql", hide=True).stdout
        if result:
            ports = re.findall(r'port=+([0-9]+)', result)
            if ports:
                return tuple(
                    sorted(set(ports))), 'Multiple instances of mysql found running, please select the port'
            else:
                return (3306,), 'Single instance of mysql found running'
        else:
            return "MySql is not running on the server", 'Error'
    except UnexpectedExit:
        return "MySql is not running ont this machine !", 'Error'

    except Exception as e:
        return str(e), 'Error'


def main_func(host, logged_user, pwd, dbtype):
    show_mysql_running_instances()
    # if dbtype == 'mysql':
    #     ports, status = show_mysql_running_instances()
    # elif dbtype == 'postgres':
    #     user = 'postgres'
    #     ports = 5432
    #     status = 'Single'
    #     dbclass = Postgres
    # else:
    #     sys.exit('\nWrong option , Exiting \n!!')
    #
    # connection_parameters = (dbclass, ports, user, status)
    # return connection_parameters

    # with Database(host, port, user, password, db_type) as db:
    #     choices = {
    #         '1': db.manage_databases,
    #         '2': db.manage_users,
    #         '3': db.manage_access,
    #         'q': lambda: sys.exit("User "
    #                               "exited")
    #     }
    #     resp = input("Press a key: ")
    #     while resp:
    #         choices.get(resp, lambda: "")()
    #         menu()
    #         resp = input("Press a key: ")


if __name__ == "__main__":
    try:
        logged_user = getuser()
        host = 'localhost'
        # password = getpass("Enter password for root user: ")
        pwd = "TowerMyDB"
        dbtype = input(
            "Which DB you want to work on Mysql(m)/Postgres(p): ").lower()
        main_func(host, logged_user, pwd, dbtype)
    except KeyboardInterrupt:
        sys.exit("\nCtrl-c issued by user !!!\n")

# todo Add entry to pg_hba.conf for new db/user - as this controls which
# user can connect to what database
