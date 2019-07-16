from ..my_math import add, subt, mul


class TestMath:
    def test_add_postive(self):
        assert add(1, 2) == 3

    def test_add_negative(self):
        assert add(-3, -5) == -4

    def test_subt(self):
        assert subt(5, 7) == -2
