import logging
import serial

logging.basicConfig(filename='app.log', level=logging.INFO)

class IoCardException(Exception):
    def _init__(self, value):
        self.message = value + "av"
    def __str__(self):
        return repr(self.value)

class UsbCard:
    ERROR_KEYWORD = "ERROR:"
    TIMEOUT = 0.05
    READ_MAX_COUNT = 200

    def __init__(self, port, speed, serialInterface=None):
        if serialInterface != None:
            self.serial_con = serialInterface.Serial(port, speed, timeout=self.TIMEOUT)
        else:
            self.serial_con = serial.Serial(port, speed, timeout=self.TIMEOUT)

    def read_terminal(self, terminal_name):
        result = self._get_result("READ " + terminal_name)

        if self.ERROR_KEYWORD in result:
            raise IoCardException("IO card returned error, error message: " + result)

        if result != "HIGH" and result != "LOW":
            raise ValueError("Result should be 'LOW' or 'HIGH', other values are invalid. Returned value: '" + result + "'")

        return result

    def set_terminal_high(self, terminal_name):
        result = self._get_result("SET " + terminal_name + " HIGH")

        if self.ERROR_KEYWORD in result:
            raise IoCardException("Error occurred during SET, error: " + self.serial_con.readline())

    def set_terminal_low(self, terminal_name):
        result = self._get_result("SET " + terminal_name + " LOW")

        if self.ERROR_KEYWORD in result:
            raise IoCardException("Error occurred during SET, error: " + self.serial_con.readline())

    def adc_of_terminal(self, terminal_name):
        result = self._get_result("ADC " + terminal_name)

        try:
            return float(result)
        except ValueError:
            raise IoCardException("Invalid value returned from IO card, value returned: " + result)

    def _get_result(self, command):
        self.serial_con.write(command+"\n")

        result = self.serial_con.read(self.READ_MAX_COUNT)

        result = result.replace(command, "") # Remove echo.
        return result.strip('\n\r\t ')

