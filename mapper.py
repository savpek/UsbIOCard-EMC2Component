# This object maps terminal IO to EMC2 component.
# update will fetch all states from IO card and update them to EMC component.
from mock import call
import hal
import iocard

def _do_nothing(x):
    return x

class Input:
    signal_name = None
    terminal_name = None
    custom_modifier = None
    pin_handle = None

    def __init__(self, terminal_name, signal_name, custom_modifier=None):
        self.terminal_name = terminal_name
        self.signal_name = signal_name
        self.custom_modifier = custom_modifier

    def map_to(self, component):
        component.newpin(self.signal_name, hal.HAL_FLOAT, hal.HAL_IN)
        pin_handle = component[self.signal_name]

    def update(self, iocard):
        pass

class HandleBase:
    signal = None
    terminal = None
    output_modifier = None

    def __init__(self, signal_handle, terminal_name, output_modifier):
        self.signal_name = signal_handle
        self.terminal_name = terminal_name
        self.output_modifier = output_modifier

class InputHandle(HandleBase):
    def io_operation(self, iocard):
        #self.signal_handle = iocard.read_terminal(self.terminal)
        pass

class OutputHandle(HandleBase):
    def io_operation(self):
        pass

class AdcHandle(HandleBase):
    def io_operation(self):
        pass

class Component:
    handles = []

    def __init__(self, iocard, component_name, injected_component=None):
        self.iocard = iocard
        self.handles = []

        if injected_component is None:
            self.component = hel.component(component_name)
        else:
            self.component = injected_component

    def update(self):
        pass

    def add_input(self, signal_name, terminal_name, output_modifier=None):
        self.component.newpin(signal_name, hal.HAL_FLOAT, hal.HAL_IN)
        self.handles.append(InputHandle(signal_name, terminal_name, output_modifier))

    def add_output(self, signal_name, terminal_name, output_modifier=None):
        self.component.newpin(signal_name, hal.HAL_FLOAT, hal.HAL_OUT)
        self.handles.append(OutputHandle(signal_name, terminal_name, output_modifier))

    def add_adc(self):
        pass

    def set_ready(self):
        pass

"""
#!/usr/bin/python
import hal, time
h = hal.component("passthrough")
h.newpin("in", hal.HAL_FLOAT, hal.HAL_IN)
h.newpin("out", hal.HAL_FLOAT, hal.HAL_OUT)
h.ready()
try:
    while 1:
        time.sleep(1)
        h['out'] = h['in']
except KeyboardInterrupt:
    raise SystemExit
"""

