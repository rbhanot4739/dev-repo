from dbConnect import query_data
import psycopg2

conn = None


def setup_module(module):
    global conn
    conn = psycopg2.connect(database='postgres', host='127.0.0.1', user='postgres', password='test123')
    print('Setting Up ')


def teardown_module(module):
    conn.close()
    print('Cleaning up !!')


def test_john():
    name = query_data(conn, 1)
    assert name == 'John'


def test_Mary():
    name = query_data(conn, 2)
    assert name == 'Mary'
