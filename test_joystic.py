import unittest
from mock import MagicMock, call
import joystic
import iocard

class UsbIoCardConnection_InitTests(unittest.TestCase):
    def setUp(self):
        self.con_mock = MagicMock(spec=iocard.UsbCard)
        self.dir_ctrl = joystic.DirController(self.con_mock)

        self.dir_ctrl.x_plus_name = "2.T0"
        self.dir_ctrl.x_minus_name = "2.T1"
        self.dir_ctrl.y_plus_name = "2.T2"
        self.dir_ctrl.y_minus_name = "2.T3"

    def test_update_calls_with_all_defined_terminals(self):
        self.dir_ctrl.update()
        expected = [call("2.T0"), call("2.T1"), call("2.T2"), call("2.T3")]
        self.assertEquals(self.con_mock.read_terminal.call_args_list, expected)

    def test_update_ignores_not_defined_terminals(self):
        self.dir_ctrl.y_plus_name = None
        self.dir_ctrl.y_minus_name = None
        self.dir_ctrl.update()

        expected = [call("2.T0"), call("2.T1")]
        self.assertEquals(self.con_mock.read_terminal.call_args_list, expected)

    def test_update_returns_values_correctly(self):
        self.con_mock.read_terminal = MagicMock(return_value=100)
        self.dir_ctrl.update()
        self.assertEquals(100, self.dir_ctrl.x_plus_value)

        self.con_mock.read_terminal = MagicMock(return_value=200)
        self.dir_ctrl.update()
        self.assertEquals(200, self.dir_ctrl.x_minus_value)