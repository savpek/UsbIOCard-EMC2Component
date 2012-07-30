import unittest
import iocard
from mock import MagicMock, call, patch
import mapper
import hal

__author__ = 'savpek'

class Input_UnitTests(unittest.TestCase):
    def setUp(self):
        pass

    def test_input_set_properties_correctly(self):
        modifier = lambda x:x
        input = mapper.Input("2.T0", "2T0", modifier)
        self.assertEqual("2.T0", input.terminal_name)
        self.assertEqual("2T0", input.signal_name)
        self.assertEqual(modifier, input.custom_modifier)

    def test_input_maps_component_correctly(self):
        component = MagicMock()
        input = mapper.Input("2.T0", "2T0")
        input.map_to(component)

        component.newpin.assert_called_once_with("2T0", hal.HAL_FLOAT, hal.HAL_IN)

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

    def test_update_updates_readed_values_to_emc_signals(self):
        self.mapper.iomap = ("2.T2", "2T2", "IN"), ("2.T3", "2T3", "IN")
        self.mapper.update()



