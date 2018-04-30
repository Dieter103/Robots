from tkinter import *
from MotorAction import *
from BodyTurnAction import *
from HeadTurnAction import *
from HeadTiltAction import *
from PauseAction import *
from PropertyEditor import *
from SpeakAction import *
from WaitForSpeechAction import *
from GameAction import *
from _thread import start_new_thread
from Server import *


import time

server = Server()


class GifFrame(object):
    def __init__(self):
        self.frameCount = 0
        self._window = Toplevel()
        self._window.attributes("-fullscreen", True)
        self.imageGIF2 = PhotoImage(file="gif.gif", format="gif -index " + str(self.frameCount))
        self.imageLabel2 = Label(self._window, image=self.imageGIF2)
        self.imageLabel2.pack()
        self.imageLabel2.place(x=master.winfo_screenwidth() / 2, y=master.winfo_screenheight() / 2, anchor=CENTER)

    def update(self):
        pass
        # try:
        #     self.imageGIF2 = PhotoImage(file="gif.gif", format="gif -index " + str(self.frameCount))
        #     self.imageLabel2.configure(image=self.imageGIF2)
        # except:
        #     print('test')
        #     self.frameCount = 0
        #     self.imageGIF2 = PhotoImage(file="gif.gif", format="gif -index " + str(self.frameCount))
        #     self.imageLabel2.configure(image=self.imageGIF2)
        # self.frameCount += 1

    def win(self):
        return self._window

    def destroy(self):
        self._window.destroy()


def center(toplevel):
    toplevel.update_idletasks()
    w = toplevel.winfo_screenwidth()
    h = toplevel.winfo_screenheight()
    size = tuple(int(_) for _ in toplevel.geometry().split('+')[0].split('x'))
    x = w/2 - size[0]/2
    y = h/2 - size[1]/2
    toplevel.geometry("%dx%d+%d+%d" % (size + (x, y)))


actions = [None] * 8

actionOptions = [MotorAction(), BodyTurnAction(), HeadTurnAction(), HeadTiltAction(), PauseAction(), WaitForSpeechAction(), SpeakAction(), GameAction()]

windowWidth = 1280
windowHeight = 720


class DragManager:
    def add_dragable(self, widget):
        widget.bind("<ButtonPress-1>", self.on_start)
        widget.bind("<B1-Motion>", self.on_drag)
        widget.bind("<ButtonRelease-1>", self.on_drop)
        widget.configure(cursor="hand1")

    def on_start(self, event):
        pass

    def on_drag(self, event):
        # you could use this method to move a floating window that
        # represents what you're dragging
        pass

    def on_drop(self, event):
        global actions
        # find the widget under the cursor
        x, y = event.widget.winfo_pointerxy()
        target = event.widget.winfo_containing(x, y)
        target.configure(image=event.widget.cget("image"))
        dropIndex = int(target.cget("text").split("\n")[0].split(" ")[1])
        dropSourceIndex = int(event.widget.cget("text"))

        print(dropIndex)
        print(dropSourceIndex)

        actions[dropIndex - 1] = actionOptions[dropSourceIndex - 1].copy()


master = Tk()

frame = Frame(master, width=windowWidth, height=windowHeight, bd=2, relief=GROOVE)
frame.pack()

dnd = DragManager()


def onActionClicked(event):
    global actions

    val = int(event.widget.cget("text").split("\n")[0].split(" ")[1])
    if actions[val - 1] is not None:
        PropertyEditor(actions[val - 1])


for i in range(len(actionOptions)):
    label = Label(frame, text=str(i + 1), image=actionOptions[i].image(), borderwidth=2, relief="groove", width=64, height=64)
    label.place(x=0, y=20 + i * 67, anchor=NW)
    dnd.add_dragable(label)

labels = []
for i in range(8):
    labelFrame = Frame(frame, width=65, height=65)
    labelFrame.pack_propagate(0)
    label = Label(labelFrame, text='Action ' + str(i + 1) + '\nDrag here!', borderwidth=2, relief="groove", width=64, height=64)
    label.pack()
    label.bind("<ButtonPress-1>", onActionClicked)
    labels.append(label)
    labelFrame.place(x=170 + 65 * i, y=(windowHeight - 64) / 2, anchor=NW)


def run_threaded():

    # controller = Controller()
    #
    for action in actions:
        if action is not None:
            action.run(None, server)
    #     else:
    #         controller.setTarget(0, 6000)
    #         controller.setTarget(1, 6000)
    #         controller.setTarget(2, 6000)
    #         controller.setTarget(3, 6000)
    #         controller.setTarget(4, 6000)



def draw_animation(sm, delay):
    sm.update()
    sm.win().after(delay, draw_animation, sm, delay)


# def run_animation():
#     duration = 0
#     for action in actions:
#         if action is not None:
#             duration += action.properties.get('Duration', (0, 0, 0))[0]
#
#     sm = GifFrame()
#     start_new_thread(draw_animation, (sm, 100))
#     time.sleep(duration)
#     sm.destroy()


def run():
    start_new_thread(run_threaded, ())
    # start_new_thread(run_animation, ())


def reset():
    global labels
    global actions
    actions = [None] * 8
    for label in labels:
        label.configure(image='')


button = Button(master, text="Run", command=run)
button.place(x=400, y=100, anchor=NW)
button = Button(master, text="Reset", command =reset)
button.place(x=500, y=100, anchor=NW)

center(master)
mainloop()
