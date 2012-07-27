import logging
import time
import iocard
import joystic

ser = iocard.UsbCard(port="COM3", speed=9600)

log = logging.getLogger('JogwheelApp')
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logHandler = logging.FileHandler('userspace_component.log')
logHandler.setFormatter(formatter)
log.addHandler(logHandler)

# Settings for XY joystic.
xy_joystic = joystic.DirController(ser)
xy_joystic.x_plus_name = "5.T1"
xy_joystic.x_minus_name = "5.T2"
xy_joystic.y_plus_name = "5.T3"
xy_joystic.y_minus_name = "5.T4"


def main():
    #try:
    while True:
        xy_joystic.update()
    #except ValueError as e:
    #    log.exception(e)

if __name__ == "__main__":
    main()