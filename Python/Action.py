from tkinter import *
# from enum import Enum
from aenum import Enum, auto
import time

from Maestro import Controller

class GuiType(Enum):
    # (SLIDER, init val, min, max)
    SLIDER = auto()
    # (TEXTBOX, init text)
    TEXTBOX = auto()
    # (DROPDOWN, init index, [options])
    DROPDOWN = auto()

class Action:
    def __init__(self):
        self.img = ""
        # Unique map of properties in format (initialValue, min, max)
        self.properties = {}
        self.propertyList = {}

    def getPropertyValue(self, property):
        return self.properties[property][0]

    def run(self, controller, server):
        pass

    def copy(self):
        pass

    # Lets us draw the image, we can't load in the image until tkinter is init
    def image(self):
        if type(self.img) is str:
            self.img = PhotoImage(file=self.img)
        return self.img
