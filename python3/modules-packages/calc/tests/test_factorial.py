import os
import sys
from random import randint

import pytest

from ..factorial import fact


@pytest.fixture(scope='class')
def pre(request):
    print('************setting up************')

    pwd = os.environ.get('PASSWD', None)
    if pwd is not None:
        print(randint(1, 100))
        request.cls.pwd = randint(1, 100)
    else:
        print(randint(1, 100))
        pytest.exit('This test requires your password, '
                    'please run export PASSWD=<yourPassword>')


@pytest.mark.usefixtures('pre')
class TestFactorial:
    def test_postive(self):
        assert fact(5) == 120

    def test_false(self):
        assert fact(6) == 720
