import unittest
from mock import MagicMock
import directiondriver

class UsbIoCardConnection_InitTests(unittest.TestCase):
    def setUp(self):
        self.connection_mock = MagicMock()
        self.dir_ctrl = directiondriver.DirController(self.connection_mock)

    def test_connection_is_opened_with_correct_arguments(self):
        pass



