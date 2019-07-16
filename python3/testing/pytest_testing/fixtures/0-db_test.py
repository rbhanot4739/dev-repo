from dbConnect import query_data
import psycopg2


def test_john():
    conn = psycopg2.connect(database='postgres', host='127.0.0.1', user='postgres', password='test123')
    cur = conn.cursor()
    name = query_data(cur, 1)
    assert name == 'John'


def test_Mary():
    conn = psycopg2.connect(database='postgres', host='127.0.0.1', user='postgres', password='test123')
    cur = conn.cursor()
    name = query_data(cur, 2)
    assert name == 'Mary'
