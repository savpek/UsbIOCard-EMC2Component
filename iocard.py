import logging
import serial

class IoCardException(Exception):
    pass

"""
 Abstraction class to command USB-IO card.
 Example:
    iocard = UsbCard("COM9", 9600)
    a = iocard.read_terminal("5.T1")
    iocard.set_terminal_high("2.T2")
    b = iocard.adc_of_termina("3.T0")
 Throws:
  Throws IO card error if connection works but result is somehow unexcepted.
"""
class UsbCard:
    ERROR_KEYWORD = "ERROR:"
    TIMEOUT = 0.05  # How long input is waited after command.
                    # This delay is kept after every command call.
    READ_MAX_COUNT = 200

    def __init__(self, port, speed, serialInterface=None):
        if serialInterface != None:
            self.serial_con = serialInterface.Serial(port, speed, timeout=self.TIMEOUT)
        else:
            self.serial_con = serial.Serial(port, speed, timeout=self.TIMEOUT)

    def read_terminal(self, terminal_name):
        result = self._get_result("READ " + terminal_name)

        self._check_for_error_keyword(result)

        if result != "HIGH" and result != "LOW":
            raise IoCardException("Result should be 'LOW' or 'HIGH', other values are invalid. Returned value: '" + result + "'")

        return result

    def set_terminal_high(self, terminal_name):
        result = self._get_result("SET " + terminal_name + " HIGH")
        self._check_for_error_keyword(result)

    def set_terminal_low(self, terminal_name):
        result = self._get_result("SET " + terminal_name + " LOW")
        self._check_for_error_keyword(result)

    def adc_of_terminal(self, terminal_name):
        result = self._get_result("ADC " + terminal_name)

        self._check_for_error_keyword(result)

        try:
            return float(result)
        except ValueError:
            raise IoCardException("Invalid value returned from IO card, value returned: " + result)

    def _get_result(self, command):
        self.serial_con.write(command+"\n")

        result = self.serial_con.read(self.READ_MAX_COUNT)

        result = result.replace(command, "") # Remove echo.
        return result.strip('\n\r\t ')

    def _check_for_error_keyword(self, result):
        if self.ERROR_KEYWORD in result:
            raise IoCardException("Result contained error keyword:" + self.serial_con.readline())

