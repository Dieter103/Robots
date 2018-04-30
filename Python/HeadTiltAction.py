from Action import *


class HeadTiltAction(Action):
    def __init__(self):
        super(HeadTiltAction, self).__init__()
        self.img = 'head_tilt.gif'

        # Properties in format (initialValue, min, max)
        self.properties['Tilt'] = (GuiType.SLIDER, 0, -5, 5)

    # Override run function
    def run(self, controller, server):
        head_tilt_step = int(self.getPropertyValue('Tilt') * 500 + 6000)
        controller.setTarget(4, head_tilt_step)
        time.sleep(1)
        print(head_tilt_step)
        pass

    def copy(self):
        return HeadTiltAction()
