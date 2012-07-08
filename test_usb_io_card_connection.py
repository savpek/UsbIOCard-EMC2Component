import unittest
from mock import MagicMock
from usb_io_card_connection import UsbCard, IOCardCmd, CmdType, CmdState, IoCardReturnError

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

    def test_send_correctly_formatted_read_message(self):
        command = IOCardCmd(CmdType.READ_PIN, "2.T0")
        self.usb_card.send_command(command)
        self.handle_mock.write.assert_called_with("READ 2.T0")

    def test_send_command_returns_correct_value_with_read_message(self):
        self.handle_mock.readLine = MagicMock(return_value = "LOW")
        command = IOCardCmd(CmdType.READ_PIN, "2.T0")
        result = self.usb_card.send_command(command)
        self.assertEquals(result.return_value, CmdState.LOW)

        self.handle_mock.readLine = MagicMock(return_value = "HIGH")
        command = IOCardCmd(CmdType.READ_PIN, "2.T0")
        result = self.usb_card.send_command(command)
        self.assertEquals(result.return_value, CmdState.HIGH)

    def test_send__command_returns_exception_on_error(self):
        self.handle_mock.readLine = MagicMock(return_value = "ERROR: INVALID TERMINAL")
        with self.assertRaises(IoCardReturnError):
            self.usb_card.send_command(IOCardCmd(CmdType.READ_PIN, "2.T0"))

    def test_send_command_correctly_formatted_set_message(self):
        command = IOCardCmd(CmdType.SET_PIN, "2.T0", CmdState.LOW)
        self.usb_card.send_command(command)
        self.handle_mock.write.assert_called_with("SET 2.T0 LOW")

        command = IOCardCmd(CmdType.SET_PIN, "2.T0", CmdState.HIGH)
        self.usb_card.send_command(command)
        self.handle_mock.write.assert_called_with("SET 2.T0 HIGH")

    def test_send_command_returns_none_as_return_value(self):
        self.handle_mock.readLine = MagicMock(return_value="")
        command = IOCardCmd(CmdType.SET_PIN, "2.T0", CmdState.LOW)
        command = self.usb_card.send_command(command)
        self.assertEquals(command.return_value, None)

    def test_send_command_adc_command_correctly_formatted(self):
        command = IOCardCmd(CmdType.READ_ADC, "2.T0")
        self.usb_card.send_command(command)
        self.handle_mock.write.assert_called_with("ADC 2.T0")
