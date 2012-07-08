import logging
import serial

logging.basicConfig(filename='app.log', level=logging.INFO)

class Pin:
    HIGH = 1
    LOW = 0

class UsbCard:
    def __init__(self, port, speed):
        pass

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
            raise Exception("IO card returned error: " + result)
        return result

