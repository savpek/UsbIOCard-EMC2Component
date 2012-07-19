import iocard

class Direction:
    # Controller one direction.
    plus_name = ""
    plus_value = ""
    minus_name = ""
    minus_value = ""

class DirController:
    directions
    connection

    def __init__(self, terminal_name, usb_connection):
        self.connection = usb_connection
        self.terminal_name = terminal_name

    def abc(self):
        pass

