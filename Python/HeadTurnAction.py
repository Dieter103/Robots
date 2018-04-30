from Action import *


class HeadTurnAction(Action):
    def __init__(self):
        super(HeadTurnAction, self).__init__()
        self.img = 'head_turn.gif'

        # Properties in format (initialValue, min, max)
        self.properties['Duration'] = (GuiType.SLIDER, 0, -5, 5)

    # Override run function
    def run(self, controller, server):
        head_step = int(self.getPropertyValue('Rotation in Degrees') * 500+6000)
        controller.setTarget(0,head_step)
        time.sleep(1)
        pass

    def copy(self):
        return HeadTurnAction()
