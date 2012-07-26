import unittest
from mock import MagicMock
from iocard import UsbCard, IoCardException

class UsbIoCardConnection_InitTests(unittest.TestCase):
    def test_connection_is_opened_with_correct_arguments(self):
        self.serial_mock = MagicMock()
        UsbCard("COM1", 9600, serialInterface=self.serial_mock)
        # Timeout must be set to 1! Otherwise readline will hang forever!
        self.serial_mock.Serial.assert_called_with("COM1", 9600, timeout=1)

class UsbIoCardConnection_Tests(unittest.TestCase):
    def setUp(self):
        self.handle_mock = MagicMock()
        self.serial_mock = MagicMock
        self.serial_mock.Serial = MagicMock(return_value=self.handle_mock)
        self.usb_card = UsbCard("COM1", 9600, serialInterface=self.serial_mock)
        self.handle_mock.inWaiting(return_value = 10)

    def test_read_terminal_sends_correctly_formatted_message(self):
        self.handle_mock.readline = MagicMock(return_value = "LOW")
        self.usb_card.read_terminal("2.T0")
        self.handle_mock.write.assert_called_with("READ 2.T0")

    def test_read_terminal_returns_values_correctly(self):
        self.handle_mock.readline = MagicMock(return_value = "LOW")
        result = self.usb_card.read_terminal("2.T0")
        self.assertEquals(result, "LOW")

        self.handle_mock.readline = MagicMock(return_value = "HIGH")
        result = self.usb_card.read_terminal("2.T0")
        self.assertEquals(result, "HIGH")

    def test_read_terminal_throws_exception_if_return_value_is_invalid(self):
        self.handle_mock.readline = MagicMock(return_value = "auu")
        with self.assertRaises(ValueError):
            self.usb_card.read_terminal("2.T0")

    def test_read_terminal_throws_exception_if_error_keyword_is_contained_in_return_value(self):
        self.handle_mock.readline = MagicMock(return_value = "ERROR: Invalid terminal name")
        with self.assertRaises(IoCardException):
            self.usb_card.read_terminal("2.T0")

    def test_set_terminal_high_send_correctly_formatted_message(self):
        self.handle_mock.readline = MagicMock(return_value = "")
        self.handle_mock.inWaiting = MagicMock(return_value = 0)
        self.usb_card.set_terminal_high("2.T0")
        self.handle_mock.write.assert_called_with("SET 2.T0 HIGH")

    def test_set_terminal_high_doesnt_call_readline_if_no_chars_in_read_buffer(self):
        self.handle_mock.readline = MagicMock(return_value = "")
        self.handle_mock.inWaiting = MagicMock(return_value = 0)
        self.usb_card.set_terminal_high("2.T0")
        self.assertFalse(self.handle_mock.readline.called)

    def set_set_terminal_high_returns_no_value(self):
        self.handle_mock.readline = MagicMock(return_value = "")
        self.handle_mock.inWaiting = MagicMock(return_value = 0)
        result = self.usb_card.set_terminal_high("2.T0")
        self.assertEquals(result, None)

    def test_set_terminal_high_any_return_from_io_card_counts_as_exception(self):
        self.handle_mock.readline = MagicMock(return_value = "")
        self.handle_mock.inWaiting(return_value=10)

        with self.assertRaises(IoCardException):
            self.usb_card.set_terminal_high("2.T3")

    def test_set_terminal_low_send_correctly_formatted_message(self):
        self.handle_mock.readline = MagicMock(return_value = "")
        self.handle_mock.inWaiting = MagicMock(return_value = 0)
        self.usb_card.set_terminal_low("2.T0")
        self.handle_mock.write.assert_called_with("SET 2.T0 LOW")

    def set_set_terminal_high_returns_no_value(self):
        self.handle_mock.readline = MagicMock(return_value = "")
        self.handle_mock.inWaiting = MagicMock(return_value = 0)
        result = self.usb_card.set_terminal_high("2.T0")
        self.assertEquals(result, None)

    def test_set_terminal_high_any_return_from_io_card_counts_as_exception(self):
        self.handle_mock.readline = MagicMock(return_value = "")
        self.handle_mock.inWaiting(return_value=10)

        with self.assertRaises(IoCardException):
            self.usb_card.set_terminal_low("2.T3")

    def test_set_terminal_high_doesnt_call_readline_if_no_chars_in_read_buffer(self):
        self.handle_mock.readline = MagicMock(return_value = "")
        self.handle_mock.inWaiting = MagicMock(return_value = 0)
        self.usb_card.set_terminal_low("2.T0")
        self.assertFalse(self.handle_mock.readline.called)

    def test_set_terminal_low_send_correctly_formatted_message(self):
        self.handle_mock.readline = MagicMock(return_value = "")
        self.handle_mock.inWaiting = MagicMock(return_value = 0)
        self.usb_card.set_terminal_low("2.T0")
        self.handle_mock.write.assert_called_with("SET 2.T0 LOW")

    def test_adc_from_terminal_send_correctly_formatted_message(self):
        self.usb_card.adc_of_terminal("2.T0")
        self.handle_mock.write.assert_called_with("ADC 2.T0")

    def test_adc_from_terminal_returns_number_from_correct_result(self):
        self.handle_mock.readline = MagicMock(return_value="0")
        self.assertEqual(self.usb_card.adc_of_terminal("2.T1"), 0)

        self.handle_mock.readline = MagicMock(return_value="100")
        self.assertEqual(self.usb_card.adc_of_terminal("2.T1"), 100)

        self.handle_mock.readline = MagicMock(return_value="256")
        self.assertEqual(self.usb_card.adc_of_terminal("2.T1"), 256)

    def test_adc_from_terminal_raise_error_if_not_number_returned(self):
        self.handle_mock.readline = MagicMock(return_value="3bx")

        with self.assertRaises(IoCardException):
            self.usb_card.adc_of_terminal("2.T2")

        self.handle_mock.readline = MagicMock(return_value="ERROR: ....")

        with self.assertRaises(IoCardException):
            self.usb_card.adc_of_terminal("2.T2")

    def _iocard_return_value(self, value):
        self.handle_mock.readline = MagicMock(return_value=value)

