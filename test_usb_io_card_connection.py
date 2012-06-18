from flexmock import flexmock
import usb_io_card_connection
import unittest

class UsbIoCardConnection_InitTests(unittest.TestCase):

    def setUp(self):
        self.serial_mock = flexmock()
        self.serial_instance = flexmock()
        self.serial_mock.should_receive('Serial')\
            .and_return(self.serial_instance)
        self.connection = usb_io_card_connection.UsbCard(self.serial_mock, 'COM1', 9600)

    def test_connection_is_opened_with_correct_arguments(self):
        expected = self.serial_mock.should_receive('Serial')\
            .with_args('COM1', 9600)\
            .and_return(self.serial_instance).once()
        usb_io_card_connection\
            .UsbCard(self.serial_mock, 'COM1', 9600)
        expected.verify()

    def test_another_thing(self):
        expected = self.serial_instance.should_call('write')\
            .and_return("LOW").once()
        return_result = self.connection.read_terminal_state("2.T0")
        unittest.Assert(
            return_result != usb_io_card_connection.Pin.LOW,
            "Invalid pin state returned"
        )

