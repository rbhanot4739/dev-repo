from dbConnect import query_data
import psycopg2, pytest


# Pytest fixture scopes

# function: Run once per test
# class: Run once per class of tests
# module: Run once per module
# session: Run once per session

# Pytest fixture using finalizer

# @pytest.fixture(scope='module')
# def conn(request):
#     print('\nSetting up')
#     db = psycopg2.connect(database='postgres', host='127.0.0.1', user='postgres', password='test123')
#
#     def cleanup():
#         db.close()
#         print('\nCleaning up')
#     request.addfinalizer(cleanup)
#     return db

# Recommended way of doing setup and teardown using yield. yield is recommended from Pytest 2.10


@pytest.fixture(scope='module')
def conn():
    print('Setting up')
    db = psycopg2.connect(database='postgres', host='127.0.0.1', user='postgres', password='test123')
    cur = db.cursor()
    yield cur
    cur.close()
    db.close()
    print('Cleaning up')


def test_john(conn):
    name = query_data(conn, 1)
    assert name == 'John'


def test_alice(conn):
    name = query_data(conn, 2)
    assert name == 'Alice'
