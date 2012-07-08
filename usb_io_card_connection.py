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

class IoCardException(Exception):
    def _init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)

class UsbCard:
    ERROR_KEYWORD = "ERROR:"
    TIMEOUT = 1

    def __init__(self, port, speed):
        self.serial_con = serial.Serial(port, speed, timeout=self.TIMEOUT)

    def __init__(self, serialInterface, port, speed):
        self.serial_con = serialInterface.Serial(port, speed, timeout=self.TIMEOUT)

    def read_terminal(self, terminal_name):
        self.serial_con.write("READ " + terminal_name)

        result = self.serial_con.readline()

        if self.ERROR_KEYWORD in result:
            raise IoCardException("IO card returned error, error message: " + result)

        if result != "HIGH" and result != "LOW":
            raise ValueError("Result should be 'LOW' or 'HIGH', other values are invalid. Returned value: " + result)
        return result

    def set_terminal_high(self, terminal_name):
        self.serial_con.write("SET "  + terminal_name + " HIGH")

        if(self.serial_con.inWaiting() != 0):
            raise IoCardException("Error occurred during SET, error: " + self.serial_con.readline())

    def set_terminal_low(self, terminal_name):
        self.serial_con.write("SET "  + terminal_name + " LOW")

        if(self.serial_con.inWaiting() != 0):
            raise IoCardException("Error occurred during SET, error: " + self.serial_con.readline())


    def adc_of_terminal(self, terminal_name):
        pass

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


