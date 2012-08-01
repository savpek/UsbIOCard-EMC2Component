# This object maps terminal IO to EMC2 component.
# update will fetch all states from IO card and update them to EMC component.
from mock import call
import hal

class HandleBase:
    def __init__(self, signal_handle, terminal_name, output_modifier=None):
        self.signal_name = signal_handle
        self.terminal_name = terminal_name

        if output_modifier is None:
            self.output_modifier = lambda x:x # Does nothing.
        else:
            self.output_modifier = output_modifier

class InputHandle(HandleBase):
    def io_operation(self, iocard, component):
        component[self.signal_name] = self.output_modifier(iocard.read_terminal(self.terminal_name))

class OutputHandle(HandleBase):
    def io_operation(self, iocard, component):
        if self.output_modifier(component[self.signal_name]):
            iocard.set_terminal_high(self.terminal_name)
        else:
            iocard.set_terminal_low(self.terminal_name)

class AdcHandle(HandleBase):
    def io_operation(self, iocard, component):
        component[self.signal_name] = self.output_modifier(iocard.adc_of_terminal(self.terminal_name))

class Component:
    handles = []

    def __init__(self, iocard, component_name, injected_component=None):
        self.iocard = iocard
        self.handles = []

        if injected_component is None:
            self.component = hal.component(component_name)
        else:
            self.component = injected_component

    def update(self):
        for x in self.handles:
            x.io_operation(self.iocard, self.component)

    def add_input(self, signal_name, terminal_name, output_modifier=None):
        self.component.newpin(signal_name, hal.HAL_FLOAT, hal.HAL_IN)
        self.handles.append(InputHandle(signal_name, terminal_name, output_modifier))

    def add_output(self, signal_name, terminal_name, output_modifier=None):
        self.component.newpin(signal_name, hal.HAL_FLOAT, hal.HAL_OUT)
        self.handles.append(OutputHandle(signal_name, terminal_name, output_modifier))

    def add_adc(self, signal_name, terminal_name, output_modifier=None):
        self.component.newpin(signal_name, hal.HAL_FLOAT, hal.HAL_IN)
        self.handles.append(AdcHandle(signal_name, terminal_name, output_modifier))

    def set_ready(self):
        self.component.ready()

