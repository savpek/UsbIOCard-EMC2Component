import unittest
import iocard
from mock import MagicMock, call
import mapper

__author__ = 'savpek'

class Component_UnitTests(unittest.TestCase):
    def setUp(self):
        self.emc_component = MagicMock()
        self.iocard = MagicMock()
        self.mapper = mapper.Component(
            self.iocard,
            "test_component",
            injected_component=self.emc_component)

    def test_update_send_read_commands_from_list_to_iocard(self):
        self.mapper.iomap = ("2.T0", "2T0", "IN"), ("2.T1", "2T1", "IN")
        self.mapper.update()
        expected = [call("2.T0"), call("2.T1")]
        self.assertEquals(self.iocard.read_terminal.call_args_list, expected)

    def test_update_send_read_commands_from_list_to_iocard_another(self):
        self.mapper.iomap = ("2.T2", "2T2", "IN"), ("2.T3", "2T3", "IN")
        self.mapper.update()
        expected = [call("2.T2"), call("2.T3")]
        self.assertEquals(self.iocard.read_terminal.call_args_list, expected)

