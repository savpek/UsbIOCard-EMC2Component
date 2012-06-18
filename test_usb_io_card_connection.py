from flexmock import flexmock
import usb_io_card_connection as usb

import unittest

class UsbIoCardConnection_UnitTests(unittest.TestCase):
    def setUp(self):
        self.pyserial_mock = flexmock()
        self.serial_instance = flexmock()

    def tearDown(self):
        pass

    def test_connection_is_opened_with_correct_arguments(self):
        self.pyserial_mock.should_receive('Serial')\
            .with_args('COM1', 9600)\
            .and_return(self.serial_instance)
        usb.UsbIoCard(self.pyserial_mock, 'COM1', 9600)
    
