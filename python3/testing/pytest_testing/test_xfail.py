# use cmdline args -rxs to see summary of results for xfail and skip

from pytest_testing.math_ops import rect_area
import pytest
from sys import platform


# Failing a test without any condition

@pytest.mark.xfail
def test_rect_area():
    assert (rect_area('20', '30') == 600)


#
#  Failing a test with some condition
# # Sometimes we want to fail mutiple tests with same condition, in those cases its better to create a custom decorator and then use that.
#
# win32 = pytest.mark.skipif(platform == 'win32', reason='This should run only on Linux')
#
@pytest.mark.xfail(platform == 'win32', reason='This should run only on Linux')
# @win32
def test_mul_big():
    assert 0


@pytest.mark.xfail(run=False)
def test_rect_perimeter():
    assert 1
