from unittest.mock import patch

import pytest

from . import SAN


@pytest.fixture
def set_mock_objects(request):
    print('Start')
    request.cls.mock_platform = patch('platform.system').start()
    request.cls.mock_os_path_exists = patch('os.path.exists').start()
    yield
    patch.stopall()
    print('Done')


@pytest.mark.usefixtures('set_mock_objects')
class TestEligible:
    san = SAN()

    def test_eligible(self):
        self.mock_platform.return_value = 'Linux'
        self.mock_os_path_exists.side_effect = lambda fc_path: True if fc_path == "/sys/class/fc_host" else False
        assert self.san.eligible()

    def test_not_eligible(self):
        self.mock_platform.return_value = 'NotLinux'
        self.mock_os_path_exists.side_effect = lambda fc_path: True if fc_path == "/sys/class/no_fc_host" else False
        assert not self.san.eligible()
