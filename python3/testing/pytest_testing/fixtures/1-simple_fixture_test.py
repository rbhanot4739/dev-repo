import pytest


# define a basic fixture

@pytest.fixture
def simple_fixture():
    print('This is a simple fixture')


# Recommended way of using fixtures using funcargs  (https://docs.pytest.org/en/latest/fixture.html)
def test_1(simple_fixture):
    print('Test1')
    assert 1 == 1


def test_2(simple_fixture):
    print('Test1')
    assert 'One' == 'One'


# You can also use `usefixtures` marker to use the fixture, this way you don't have to pass the fixture to function
# this is ideal for classes
@pytest.mark.usefixtures('simple_fixture')
def test_3():
    print('Test3')
    assert 3 == 3
