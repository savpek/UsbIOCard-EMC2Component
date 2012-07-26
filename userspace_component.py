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

def main():
    jo = joystic.DirController(ser)
    jo.x_minus_name = "2.T1"
    jo.y_minus_name = "2.T2"
    #try:
    while True:
        jo.update()
        print jo.x_minus_value
        time.sleep(3)
    #except ValueError as e:
    #    log.exception(e)

if __name__ == "__main__":
    main()