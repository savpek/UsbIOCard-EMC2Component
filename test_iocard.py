import unittest
from mock import MagicMock
from iocard import UsbCard, IoCardException

class UsbIoCardConnection_InitTests(unittest.TestCase):
    def test_connection_is_opened_with_correct_arguments(self):
        self.serial_mock = MagicMock()
        UsbCard("COM1", 9600, serialInterface=self.serial_mock)
        # Timeout must be set! Otherwise terminal will hang forever.
        self.serial_mock.Serial.assert_called_with("COM1", 9600, timeout=0.05)

class UsbIoCardConnection_Tests(unittest.TestCase):
    def setUp(self):
        self.handle_mock = MagicMock()
        self.serial_mock = MagicMock()
        self.serial_mock.Serial = MagicMock(return_value=self.handle_mock)
        self.usb_card = UsbCard("COM1", 9600, serialInterface=self.serial_mock)
        self.handle_mock.inWaiting(return_value = 10)
        self._set_return_value("")

    def test_read_terminal_sends_correctly_formatted_message(self):
        self._expect_output_to_io(self.usb_card.read_terminal, "READ 2.T0\n", "2.T0", iocard_returns="HIGH")

    def test_read_terminal_returns_values_correctly(self):
        self._except_value(self.usb_card.read_terminal, "LOW", "LOW")
        self._except_value(self.usb_card.read_terminal, "HIGH", "HIGH")

    def test_read_terminal_throws_exception_if_return_value_is_invalid(self):
        self._set_return_value("something random shit.")
        with self.assertRaises(ValueError):
            self.usb_card.read_terminal("2.T0")

    def test_read_terminal_throws_exception_if_error_keyword_is_contained_in_return_value(self):
        self._test_method_with_error_returned(self.usb_card.read_terminal)

    def test_read_terminal_works_with_echo(self):
        self._except_value(self.usb_card.read_terminal, "HIGH", "READ 2.T0\n\rHIGH")
        self._except_value(self.usb_card.read_terminal, "HIGH", "READ 2.T0\nHIGH")
        self._except_value(self.usb_card.read_terminal, "HIGH", "READ 2.T0\rHIGH")

    def test_set_terminal_high_send_correctly_formatted_message(self):
        self._expect_output_to_io(self.usb_card.set_terminal_high, "SET 2.T0 HIGH\n", "2.T0")

    def test_set_terminal_high_returns_no_value(self):
        self._except_value(self.usb_card.set_terminal_high, None, "")

    def test_set_terminal_high_throw_error_if_error_keyword_in_result(self):
        self._test_method_with_error_returned(self.usb_card.set_terminal_high)

    def test_set_terminal_low_send_correctly_formatted_message(self):
        self._expect_output_to_io(self.usb_card.set_terminal_low, "SET 2.T0 LOW\n", "2.T0")

    def test_set_terminal_low_returns_no_value(self):
        self._except_value(self.usb_card.set_terminal_low, None, "")

    def test_set_terminal_low_throw_error_if_error_keyword_in_result(self):
        self._test_method_with_error_returned(self.usb_card.set_terminal_low)


    def test_adc_from_terminal_send_correctly_formatted_message(self):
        self._expect_output_to_io(self.usb_card.adc_of_terminal, "ADC 2.T0\n", "2.T0", iocard_returns="0")

    def test_adc_from_terminal_returns_number_from_correct_result(self):
        self._except_value(self.usb_card.adc_of_terminal, 0, "0")
        self._except_value(self.usb_card.adc_of_terminal, 100, "100")
        self._except_value(self.usb_card.adc_of_terminal, 256, "256")

    def test_adc_from_terminal_raise_error_if_not_number_returned(self):
        self._set_return_value("This is not number i think?")

        with self.assertRaises(IoCardException):
            self.usb_card.adc_of_terminal("2.T2")

    def test_adc_from_terminal_works_with_echo(self):
        self._except_value(self.usb_card.adc_of_terminal, 100, "ADC 2.T0\n\r100")


    def _set_return_value(self, value):
        self.handle_mock.read = MagicMock(return_value=value)

    def _except_value(self, method, expected_result, value_from_iocard=""):
        self._set_return_value(value_from_iocard)
        self.assertEqual(method("2.T0"), expected_result)

    def _expect_output_to_io(self, method, expected_value, terminal_name, iocard_returns=""):
        self.handle_mock.inWaiting(return_value=len(iocard_returns))
        self._set_return_value(iocard_returns)
        method(terminal_name)
        self.handle_mock.write.assert_called_with(expected_value)

    def _test_method_with_error_returned(self, method):
        self._set_return_value("ERROR: .....")
        with self.assertRaises(IoCardException):
            method("5.T0")

