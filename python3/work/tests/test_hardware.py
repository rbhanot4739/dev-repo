import os

import pytest

from ..hardware import (MappingError, SerialError, SerialPasswordError,
                        serial_console_checker)


@pytest.fixture(scope='class')
def set_password(request):
    pwd = os.environ.get('PASSWD', None)
    if pwd is not None:
        request.cls.pwd = pwd
    else:
        pass
        pytest.skip('This test requires your password, '
                    'please run export PASSWD=<yourPassword>')


@pytest.mark.usefixtures('set_password')
class TestSerialConsole:
    def test_console_ok_hostname_ok(self):
        assert 'matches with hostname' in serial_console_checker(
            'systems1.gurg-off', pwd=self.pwd)

    @pytest.mark.skip('No host to test')
    def test_console_ok_hostname_not_ok(self):
        assert 'does not match' in serial_console_checker('', pwd=self.pwd)

    def test_serial_password(self):
        with pytest.raises(SerialPasswordError):
            serial_console_checker('install190.gurg-off', pwd='wrong-password')

    def test_serial_error(self):
        with pytest.raises(SerialError):
            serial_console_checker('install170.asx', pwd=self.pwd)

    def test_mapping_error(self):
        with pytest.raises(MappingError):
            serial_console_checker('install161.gurg-off', pwd=self.pwd)
