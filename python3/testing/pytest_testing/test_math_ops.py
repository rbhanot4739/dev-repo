# To only run tests with specific word run from command line with -k option
# To run tets with custom markers use the -m option from cmd line
# 'python -m pytest -m "ints" -v test_math_ops.py' - to run tests for custom marker `ints`
# 'python -m pytest -m "not ints" -v test_math_ops.py' - to run all other tests except for custom marker `ints`

from pytest_testing.math_ops import rect_area, mul
import pytest


@pytest.mark.ints
def test_area_ints():
    assert (rect_area(10, 20) == 200)


def test_area_strs():
    assert (rect_area('10', '20') == 200)


@pytest.mark.ints
def test_mul_ints():
    assert (mul(4, 5) == 20)


def test_mul_strs():
    assert (mul('hello', 5) == 'hellohellohellohellohello')
