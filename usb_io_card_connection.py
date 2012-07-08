import logging
import serial

logging.basicConfig(filename='app.log', level=logging.INFO)

class CmdState:
    HIGH = "HIGH"
    LOW = "LOW"
    NA = ""

class CmdType:
    READ_PIN = "READ"
    SET_PIN = "SET"
    READ_ADC = "ADC"

class IOCardCmd:
    def __init__(self, command_type, terminal_name, state=CmdState.NA):
        self.type = command_type
        self.terminal = terminal_name
        self.state = state
    return_value = None

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

    def _check_for_error(self, feedback_line):
        if "ERROR:" in feedback_line:
            logging.error("Error occurred while running command, error string: {0}"
                .format(feedback_line))
            pass

        self.serial_con.write("Test message")

    def send_command(self, command):
        command_str = "{0} {1} {2}".format(command.type, command.terminal, command.state)
        command_str = command_str.strip()
        self.serial_con.write(command_str)
        command.return_value = self.serial_con.readLine()

        if "ERROR: " in command.return_value:
            raise IoCardReturnError("IO card returned error: " + command.return_value)

        if command.return_value == '':
            command.return_value = None

        return command


