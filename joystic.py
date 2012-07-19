import iocard

class DirController:
    y_plus_name = None
    y_minus_name = None
    x_plus_name = None
    x_minus_name = None

    x_plus_value = None
    x_minus_value = None
    y_plus_value = None
    y_minus_value = None

    def __init__(self, usb_connection):
        self.connection = usb_connection

    def update(self):
        if self.x_plus_name is not None:
            self.x_plus_value = self.connection.read_terminal(self.x_plus_name)
        if self.x_minus_name is not None:
            self.x_minus_value = self.connection.read_terminal(self.x_minus_name)
        if self.y_plus_name is not None:
            self.y_plus_name = self.connection.read_terminal(self.y_plus_name)
        if self.y_minus_name is not None:
            self.y_minus_name = self.connection.read_terminal(self.y_minus_name)

