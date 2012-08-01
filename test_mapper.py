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

    def test_outputhandle_custom_modifier_works_correctly(self):
        self.component = {'2T0':False}
        under_test = mapper.OutputHandle("2T0", "2.T0", lambda x: not x) # Simply inverts result.
        under_test.io_operation(self.iocard, self.component)
        self.iocard.set_terminal_high.assert_called_once_with("2.T0") # Notice inverted call.

    def test_adchandle_reads_and_sets_value_correctly(self):
        self.component = {'2T1':"NOT SET"}
        self.iocard.adc_of_terminal = MagicMock(return_value=200)

        under_test = mapper.AdcHandle("2T1", "2.T1", None)
        under_test.io_operation(self.iocard, self.component)
        self.iocard.adc_of_terminal.assert_called_once_with("2.T1")
        self.assertEquals(200, self.component['2T1'])

    def test_adchandle_work_with_custom_modifier(self):
        self.component = {'2T1':"NOT SET"}
        self.iocard.adc_of_terminal = MagicMock(return_value=200)

        under_test = mapper.AdcHandle("2T1", "2.T1", lambda x:3*x)
        under_test.io_operation(self.iocard, self.component)
        self.assertEquals(600, self.component['2T1'])

class Component_UnitTests(unittest.TestCase):
    def setUp(self):
        self.emc_component = MagicMock()
        self.iocard = MagicMock()
        self.mapper = mapper.Component(
            self.iocard,
            "test_component",
            injected_component=self.emc_component)

    def test_add_input_adds_handle_and_creates_pin(self):
        self.mapper.add_input("2T0", "2.T0")
        self.emc_component.newpin.assert_called_once_with("2T0", hal.HAL_FLOAT, hal.HAL_IN)
        self.assertEquals(self.mapper.handles[0].__class__.__name__, "InputHandle")
        self.assertEquals(self.mapper.handles[0].terminal_name, "2.T0")
        self.assertEquals(self.mapper.handles[0].signal_name, "2T0")

    def test_add_output_adds_handle_and_creates_pin(self):
        self.mapper.add_output("2T0", "2.T0")
        self.emc_component.newpin.assert_called_once_with("2T0", hal.HAL_FLOAT, hal.HAL_OUT)
        self.assertEquals(self.mapper.handles[0].__class__.__name__, "OutputHandle")
        self.assertEquals(self.mapper.handles[0].terminal_name, "2.T0")
        self.assertEquals(self.mapper.handles[0].signal_name, "2T0")

    def test_add_adc_adds_handle_and_creates_pin(self):
        self.mapper.add_adc("2T0", "2.T0")
        self.emc_component.newpin.assert_called_once_with("2T0", hal.HAL_FLOAT, hal.HAL_IN)
        self.assertEquals(self.mapper.handles[0].__class__.__name__, "AdcHandle")
        self.assertEquals(self.mapper.handles[0].terminal_name, "2.T0")
        self.assertEquals(self.mapper.handles[0].signal_name, "2T0")

    def test_update_runs_io_operation_for_all_items_in_list(self):
        item1 = MagicMock(mapper.InputHandle)
        item2 = MagicMock(mapper.OutputHandle)
        item3 = MagicMock(mapper.OutputHandle)
        self.mapper.handles.append(item1)
        self.mapper.handles.append(item2)
        self.mapper.handles.append(item3)
        self.mapper.update()
        self.assert_(item1.io_operation.called)
        self.assert_(item2.io_operation.called)
        self.assert_(item3.io_operation.called)


