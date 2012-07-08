import unittest
from mock import MagicMock
from usb_io_card_connection import UsbCard

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
        
    def test_send_sends_message(self):
        self.handle_mock.write = MagicMock()
        usb_card = UsbCard(self.serial_mock, "COM1", 9600)
        usb_card.send("Test message")
        self.handle_mock.write.assert_called_with("Test message")


