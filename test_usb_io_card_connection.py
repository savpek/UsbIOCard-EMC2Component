import unittest
from mock import MagicMock
from usb_io_card_connection import UsbCard

class UsbIoCardConnection_InitTests(unittest.TestCase):
    def setUp(self):
        pass
    def test_connection_is_opened_with_correct_arguments(self):
        serial_mock = MagicMock()
        serial_mock.Serial("COM1", 9600)
        usb_card = UsbCard(serial_mock, "COM1", 9600)
        serial_mock.Serial.assert_called_with("COM1", 9600)




