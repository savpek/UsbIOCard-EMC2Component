import unittest
import iocard
from mock import MagicMock, call, patch
import mapper
import hal

class Component2_UnitTests(unittest.TestCase):
    def setUp(self):
        self.component = {'2T1':"NOT SET"} # Simulates hal component signals as dictionary behavior.
        self.iocard = MagicMock()

    def test_inputhandle_io_set_readed_value_to_signal(self):
        self.iocard.read_terminal = MagicMock(return_value="EXPECTED")

        under_test = mapper.InputHandle("2T1", "2.T0", None)
        under_test.io_operation(self.iocard, self.component)

        self.iocard.read_terminal.assert_called_once_with("2.T0")
        self.assertEquals(self.component["2T1"], "EXPECTED")

    def test_inputhandle_io_custom_modifier_function_works(self):
        self.iocard.read_terminal = MagicMock(return_value=100)

        under_test = mapper.InputHandle("2T1", "2.T0", lambda x:2*x)
        under_test.io_operation(self.iocard, self.component)

        self.assertEquals(self.component["2T1"], 200)

    def test_outputhandle_send_high_signal_correctly_to_output(self):
        self.component = {'2T1':True}
        under_test = mapper.OutputHandle("2T1", "2.T1", None)
        under_test.io_operation(self.iocard, self.component)
        self.iocard.set_terminal_high.assert_called_once_with("2.T1")

    def test_outputhandle_send_low_signal_correctly_to_output(self):
        self.component = {'2T0':False}
        under_test = mapper.OutputHandle("2T0", "2.T0", None)
        under_test.io_operation(self.iocard, self.component)
        self.iocard.set_terminal_low.assert_called_once_with("2.T0")

class Component_UnitTests(unittest.TestCase):
    def setUp(self):
        self.emc_component = MagicMock()
        self.iocard = MagicMock()
        self.mapper = mapper.Component(
            self.iocard,
            "test_component",
            injected_component=self.emc_component)

    def test_add_input_doesnt_require_modifier_funtion(self):
        self.mapper.add_input("Anything", "Anything")

    def test_add_input_appends_input_handle_to_list(self):
        self.mapper.add_input("2T0", "2.T0")
        self.assertEquals(self.mapper.handles[0].__class__.__name__, "InputHandle")

    def test_add_input_set_fields_correctly(self):
        testf = lambda x:2*x
        self.mapper.add_input("2T2", "2.T2", testf)
        self.assertEqual(self.mapper.handles[0].terminal_name, "2.T2")
        self.assertEqual(self.mapper.handles[0].signal_name, "2T2")
        self.assertEquals(self.mapper.handles[0].output_modifier, testf)

    def test_add_input_creates_new_pin_to_component(self):
        self.mapper.add_input("2T3", "2.T3")
        self.emc_component.newpin.assert_called_once_with("2T3", hal.HAL_FLOAT, hal.HAL_IN)

    def test_add_output_doesnt_require_modifier_function(self):
        self.mapper.add_input("Anything", "Anything")

    def test_add_output_appends_input_handle_to_list(self):
        self.mapper.add_output("2T0", "2.T0")
        self.assertEquals(self.mapper.handles[0].__class__.__name__, "OutputHandle")

    def test_add_output_set_fields_correctly(self):
        testf = lambda x:2*x
        self.mapper.add_output("2T2", "2.T2", testf)
        self.assertEqual(self.mapper.handles[0].terminal_name, "2.T2")
        self.assertEqual(self.mapper.handles[0].signal_name, "2T2")
        self.assertEquals(self.mapper.handles[0].output_modifier, testf)

    def test_add_output_creates_new_pin_to_component(self):
        self.mapper.add_output("2T3", "2.T3")
        self.emc_component.newpin.assert_called_once_with("2T3", hal.HAL_FLOAT, hal.HAL_OUT)

