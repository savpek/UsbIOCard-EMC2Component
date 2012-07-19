import iocard

class DirController:
    y_plus_name = None
    y_minus_name = None
    x_plus_name = None
    x_minus_name = None

    def __init__(self, usb_connection):
        self.connection = usb_connection

    def update(self):
        self.connection.read_terminal(self.x_plus_name)
        self.connection.read_terminal(self.x_minus_name)
        self.connection.read_terminal(self.y_plus_name)
        self.connection.read_terminal(self.y_minus_name)

