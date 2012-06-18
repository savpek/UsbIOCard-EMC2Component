import serial

class UsbIoCard():
    def _init_serial_port(self, port, speed):
        self.serialConnection.Serial(port, speed)

    def __init__(self, port, speed):
        self._init_serial_port(port, speed)

    def __init__(self, serialInterface, port, speed):
        self.serialConnection = serialInterface
        self._init_serial_port(port, speed)

    def _sendCommand(self):
        return 33
