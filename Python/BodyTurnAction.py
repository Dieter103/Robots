from Action import *


class BodyTurnAction(Action):
    def __init__(self):
        super(BodyTurnAction, self).__init__()
        self.img = 'turn_body.gif'

        # Properties in format (initialValue, min, max)
        self.properties['Rotation Direction'] = (GuiType.DROPDOWN, 'left', ['left', 'right'])
        self.properties['Duration'] = (GuiType.SLIDER, 1000, 0, 10000)

    # Override run function
    def run(self, controller, server):
        duration = self.getPropertyValue('Duration')/1000
        if self.getPropertyValue('Rotation Direction') == 'right':
            controller.setAccel(2, 6)
            controller.setTarget(2, 5000)
            time.sleep(duration)
            pass
        else:
            controller.setAccel(2, 6)
            controller.setTarget(2, 7000)
            time.sleep(duration)
            pass

    def copy(self):
        return BodyTurnAction()
