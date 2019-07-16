from pytest_testing.math_ops import mul, rect_area, rect_perimeter
import pytest
from sys import platform


# Skipping a test without any condition

@pytest.mark.skip
def test_rect_area():
    assert (rect_area(20, 30) == 600)


# Skipping a test with some condition
# Sometimes we want to skip mutiple tests with same condition, in those cases its better to create a custom decorator and then use that.

win32 = pytest.mark.skipif(platform == 'win32', reason='This should run only on Linux')


# @pytest.mark.skipif(platform == 'win32', reason='This should run only on Linux')
@win32
def test_mul_big():
    assert (mul(10000, 20000) == 200000000)


@win32
# @pytest.mark.skipif(platform == 'win32', reason='This should run only on Linux')
def test_another_skip():
    assert 0


def test_rect_perimeter():
    assert (rect_perimeter(20, 30) == 600)


def test_mul_small():
    assert (mul(10, 20) == 200)
