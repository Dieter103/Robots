from tkinter import *
from Action import GuiType

windowWidth = 500
windowHeight = 720


def center(toplevel):
    toplevel.update_idletasks()
    w = toplevel.winfo_screenwidth()
    h = toplevel.winfo_screenheight()
    size = tuple(int(_) for _ in toplevel.geometry().split('+')[0].split('x'))
    x = w/2 - size[0]/2
    y = h/2 - size[1]/2
    toplevel.geometry("%dx%d+%d+%d" % (size + (x, y)))


class PropertyEditor:
    def __init__(self, action):
        master = Toplevel()

        self.extra = 0
        self.components = []
        for i in range(len(action.properties.keys())):
            key = list(action.properties.keys())[i]

            # needs to be redefined in oncommit
            gui_type = action.properties[key][0]

            def onCommit(val):
                keys = list(action.properties.keys())
                for n in range(len(self.components)):
                    props = action.properties[keys[n]]

                    if props[0] == GuiType.SLIDER:
                        action.properties[keys[n]] = (GuiType.SLIDER, self.components[n].get(), props[1], props[2])
                    elif props[0] == GuiType.DROPDOWN:
                        action.properties[keys[n]] = (GuiType.DROPDOWN, val, props[2])
                    elif props[0] == GuiType.TEXTBOX:
                        action.properties[keys[n]] = (GuiType.TEXTBOX, self.components[n].get())

            def addScale():
                _, value, start, end = action.properties[key]
                self.components.append(Scale(master, label=str(key), from_=start, to=end, resolution=0.1, orient=HORIZONTAL, command=onCommit))
                self.components[-1].grid(row=i + self.extra, column=0, sticky='ew', columnspan=2)
                self.components[-1].set(value)

            def addDropDown():
                _, value, options = action.properties[key]
                tkvar = StringVar(master)
                tkvar.set(value)
                Label(master, text=str(key)).grid(row=i + self.extra, column=0, sticky='ew', columnspan=2)
                self.extra = self.extra + 1
                self.components.append(OptionMenu(master, tkvar, *options, command=onCommit))
                self.components[-1].grid(row=i + self.extra, column=0, sticky='ew', columnspan=2)

            def addTextBox():
                _, value = action.properties[key]
                sv = StringVar()
                sv.trace("w", lambda name, index, mode, sv=sv: onCommit(sv))
                Label(master, text=str(key)).grid(row=i + self.extra, column=0, sticky='ew', columnspan=2)
                self.extra = self.extra + 1
                self.components.append(Entry(master, textvariable=sv))
                self.components[-1].grid(row=i + self.extra, column=0, sticky='ew', columnspan=2)
                self.components[-1].insert(END, value)

            {
                GuiType.SLIDER: addScale,
                GuiType.DROPDOWN: addDropDown,
                GuiType.TEXTBOX: addTextBox
            }[gui_type]()

        Frame(master, width=windowWidth, height=windowHeight, bd=2, relief=GROOVE)
        center(master)
