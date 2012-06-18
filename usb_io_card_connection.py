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
        #self._flush_serial()
        #logging.debug('Sending command "{0}"'.format(command_string))
        #self.serial_con.write(command_string)
        #self._check_for_error(self.serialConnection.readline())
        #return self.serialConnection.readLine()
        pass

    def _check_for_error(self, feedback_line):
        if "ERROR:" in feedback_line:
            logging.error("Error occurred while running command, error string: {0}"
                .format(feedback_line))
            pass

    def read_terminal_state(self, terminal_identifier):
        command_result = self._send_command("READ {0}".format(terminal_identifier))
        #if "LOW" in command_result:
        #    return Pin.LOW
        #else:
        #    return Pin.HIGH
        pass

    def read_terminal_adc(selfs, terminal_identifier):
        pass

    def set_terminal(self, terminal_identifier):
        pass