# This object maps terminal IO to EMC2 component.
# update will fetch all states from IO card and update them to EMC component.
from mock import call
import iocard

def hal(component_name):
    pass

class Component:
    iomap = ()

    def __init__(self, iocard, component_name, injected_component=None):
        self.iocard = iocard

        if injected_component is not None:
            pass
        else:
            self.component = hal.component(component_name)

    def update(self):
        for io in self.iomap:
            self.iocard.read_terminal(io[0])

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

