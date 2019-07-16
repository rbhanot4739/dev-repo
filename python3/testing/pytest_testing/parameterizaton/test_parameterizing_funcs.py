from math_ops import mul
import pytest


# Typical way of running tests with multiple inputs !! Not recommended !!
# def test_mul():
#      assert mul(1, 2) == 2
#      assert mul(2, 5) == 10
#      assert mul('a', 5) == 'aaaa'
#

@pytest.mark.parametrize('arg1, arg2, res',
                         [(1, 2, 2), (2, 5, 10), ('a', 5, 'aaaaa'), ('hello', 'world', 'helloworld')])
def test_mul(arg1, arg2, res):
    assert mul(arg1, arg2) == res
