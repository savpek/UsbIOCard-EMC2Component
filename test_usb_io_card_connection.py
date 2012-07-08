import unittest
from mock import MagicMock
from usb_io_card_connection import UsbCard, IoCardReturnError

class UsbIoCardConnection_InitTests(unittest.TestCase):
    def setUp(self):
        self.serial_mock = MagicMock()
    def test_connection_is_opened_with_correct_arguments(self):
        self.serial_mock.Serial = MagicMock()
        usb_card = UsbCard(self.serial_mock, "COM1", 9600)
        self.serial_mock.Serial.assert_called_with("COM1", 9600)

class UsbIoCardConnection_Tests(unittest.TestCase):
    def setUp(self):
        self.handle_mock = MagicMock()
        self.serial_mock = MagicMock
        self.serial_mock.Serial = MagicMock(return_value=self.handle_mock)
        self.usb_card = UsbCard(self.serial_mock, "COM1", 9600)

    def test_send_sends_message(self):
        self.handle_mock.write = MagicMock()
        self.usb_card.send("Test message")
        self.handle_mock.write.assert_called_with("Test message")

    def test_send_command_returns_result(self):
        self.handle_mock.readLine = MagicMock(return_value = "RETURN STRING FROM IO CARD")
        self.assertEqual(self.usb_card.send("ABC"), "RETURN STRING FROM IO CARD")

    def test_send_returns_error_keyword(self):
        self.handle_mock.readLine = MagicMock(return_value = "ERROR: INVALID SYNTAX")
        with self.assertRaises(IoCardReturnError):
            self.usb_card.send("abc")

    def test_send_flush_old_messages_before_return_result(self):
        pass
