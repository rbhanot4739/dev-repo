# http://initd.org/psycopg/docs/usage.html - Module Documentation

import psycopg2


def drop_table(cur):
    try:
        cur.execute('drop table IF EXISTS employee')
        print('Table has been dropped !!')
    except Exception as e:
        print(e)


def create_table(cur):
    try:
        cur.execute('create table employee(ID INT PRIMARY KEY, NAME VARCHAR(30) NOT NULL)')
        print('Table created successfully !!')
    except Exception as e:
        print(e)


def insert_data(cur, emp=None):
    emps = ((1, 'John'), (2, 'Alice'), (3, 'Mary'))
    try:
        # Inserting many records at once
        cur.executemany('insert into employee(ID, NAME) values (%s, %s)', emps)
        # Inserting a single record
        cur.execute('insert into employee(ID, NAME) values (%s, %s)', emp)
        conn.commit()
    except Exception as e:
        print(e)


def query_data(cur, id):
    cur.execute('Select * from employee WHERE ID=(%s)', (id,))
    name = cur.fetchone()[1]
    return name


def query_all(cur):
    cur.execute('select * from employee')
    rows = cur.fetchall()
    for row in rows:
        print(row)


if __name__ == '__main__':
    try:
        conn = psycopg2.connect(database='postgres', host='127.0.0.1', user='postgres', password='test123')
        cur = conn.cursor()
    except Exception as e:
        print(e)
    else:
        drop_table(cur)
        create_table(cur)
        insert_data(cur, (4, 'Nathon'))
        name = query_data(cur, 1)
        print('The name is ', name)
        query_all(cur)
        cur.close()
        conn.close()
