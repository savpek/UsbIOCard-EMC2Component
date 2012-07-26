import logging
import serial

logging.basicConfig(filename='app.log', level=logging.INFO)

class IoCardException(Exception):
    def _init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)

class UsbCard:
    ERROR_KEYWORD = "ERROR:"
    TIMEOUT = 1

    def __init__(self, port, speed, serialInterface=None):
        if serialInterface != None:
            self.serial_con = serialInterface.Serial(port, speed, timeout=self.TIMEOUT)
        else:
            self.serial_con = serial.Serial(port, speed, timeout=self.TIMEOUT)


    def read_terminal(self, terminal_name):
        self.serial_con.write("READ " + terminal_name)

        result = self.serial_con.readline()

        if self.ERROR_KEYWORD in result:
            raise IoCardException("IO card returned error, error message: " + result)

        if result != "HIGH" and result != "LOW":
            raise ValueError("Result should be 'LOW' or 'HIGH', other values are invalid. Returned value: '" + result + "'")
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
        self.serial_con.write("ADC " + terminal_name)

        received_line = self.serial_con.readline()

        try:
            return float(received_line)
        except (ValueError):
            raise IoCardException("Invalid value returned from IO card, value returned: " + received_line)



