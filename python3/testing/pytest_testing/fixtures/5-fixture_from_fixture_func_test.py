import pytest, sys
from psycopg2 import connect

sys.path.append(r'C:\Rohit\Study\Python\Python_my_Projects\Intermediate\unitTesting\pytest_testing')
from fixtures.dbConnect import query_data


@pytest.fixture(scope='module')
def conn():
    db = connect(host='127.0.0.1', database='postgres', user='postgres', password='test123')
    yield db
    db.close()


@pytest.fixture(scope='module')
def cur(conn):
    curs = conn.cursor()
    yield curs
    curs.close()


def test_query(cur):
    res = query_data(cur, 1)
    assert (res == 'John')
