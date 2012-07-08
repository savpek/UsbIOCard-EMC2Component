import logging
import serial

logging.basicConfig(filename='app.log', level=logging.INFO)

class CommandType:
    READ_PIN = 0
    SET_PIN = 1
    READ_ADC = 2

class Command:
    type = CommandType.READ_PIN
    pin_name = ""
    return_value = 0

class IoCardReturnError(Exception):
    def _init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)

class UsbCard:
    def __init__(self, port, speed):
        self.serial_con = serial.Serial(port, speed)

    def __init__(self, serialInterface, port, speed):
        self.serial_con = serialInterface.Serial(port, speed)

    def _flush_serial(self):
        flushed_data = self.serial_con.readLine()
        logging.debug('Flushed serial data, data in buffer: {0}'.format(flushed_data))

    def _send_command(self, command_string):
        self.serial_con.write("abc")
        pass

    def _check_for_error(self, feedback_line):
        if "ERROR:" in feedback_line:
            logging.error("Error occurred while running command, error string: {0}"
                .format(feedback_line))
            pass

        self.serial_con.write("Test message")
    def send(self, message):
        self.serial_con.write("Test message")
        result = self.serial_con.readLine()
        if "ERROR:" in result:
            raise IoCardReturnError("IO card returned error: " + result)
        return result

