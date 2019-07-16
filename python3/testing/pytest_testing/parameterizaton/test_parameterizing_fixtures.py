import pytest
import sys

sys.path.append(r'C:\Rohit\Study\Python\Python_my_Projects\Intermediate\unitTesting\pytest_testing')

from fixtures.dbConnect import query_data
from psycopg2 import connect


# This fixture will run multiple times with diff parameters specified by params=[] list.
@pytest.fixture(scope='module', params=[('postgres', 'postgres'), ('testdb', 'test1')])
def conn(request):
    dbs, usr = request.param  # This will unpack every tuple in the param list
    db = connect(host='127.0.0.1', database=dbs, user=usr, password='test123')
    cur = db.cursor()
    yield cur
    print('Cleaning Up !!')
    cur.close()
    db.close()


def test_john(conn):
    res = query_data(conn, 1)
    assert res == 'John'
