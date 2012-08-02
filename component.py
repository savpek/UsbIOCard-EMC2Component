import logging
import iocard
import mapper

log = logging.getLogger('JogwheelApp')
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logHandler = logging.FileHandler('userspace_component.log')
logHandler.setFormatter(formatter)
log.addHandler(logHandler)

usb_card = iocard.UsbCard("COM9", 9600)

iomap = mapper.Handler(usb_card, "ComponentUsbIoCard")
iomap.add_input("5T0", "5.T0")
iomap.add_input("5T1", "5.T1")
iomap.add_input("5T2", "5.T2")
iomap.add_input("5T3", "5.T3")
iomap.add_input("5T4", "5.T4")
iomap.add_input("5T5", "5.T5")
iomap.add_input("5T6", "5.T6")
iomap.add_input("5T7", "5.T7")
iomap.add_input("5T8", "5.T8")
iomap.add_input("5T9", "5.T9")
iomap.add_input("5T10", "5.T10")
iomap.add_input("5T11", "5.T11")
iomap.add_output("2T0", "2.T0")
iomap.add_output("2T1", "2.T1")
iomap.add_output("2T2", "2.T2")
iomap.add_output("2T3", "2.T3")
iomap.add_adc("ADC0","2.T0.ADC0", lambda x:10*x)
iomap.add_adc("ADC1","2.T0.ADC1", lambda x:10*x)

def main():
    try:
        while True:
            iomap.update()
    except iocard.IoCardException as e:
        log.exception(e)

if __name__ == "__main__":
    main()