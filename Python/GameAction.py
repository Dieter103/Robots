from Action import *
from Game import *


class GameAction(Action):

    def __init__(self):
        self.img = 'turn_body.gif'

        pass

    # Override run function
    def run(self, controller, server):
        go(controller,server)

        pass

    def copy(self):
        return GameAction()
