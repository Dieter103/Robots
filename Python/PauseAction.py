import time
from Action import *


class PauseAction(Action):
    def __init__(self):
        super(PauseAction, self).__init__()
        self.img = 'timer.gif'

        # Properties in format (initialValue, min, max)
        self.properties['Duration'] = (GuiType.SLIDER, 0, 0, 10)

    # Override run function
    def run(self, controller, server):
        print('timer start - running for', float(self.properties['Duration'][0]), 'seconds')
        controller.setTarget(0, 6000)
        controller.setTarget(1, 6000)
        controller.setTarget(2, 6000)
        controller.setTarget(3, 6000)
        controller.setTarget(4, 6000)
        time.sleep(self.getPropertyValue('Duration'))
        print('timer end')
        pass

    def copy(self):
        return PauseAction()
