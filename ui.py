from Tkinter import *
from threading import Thread

import bgb

connected = False

def key(event):
    print "pressed", event.keysym

def key_release(event):
    print "release", event.keysym

has_focus = False

def update_text():
    if connected:
        if has_focus:
            s = "Keyjazz!"
        else:
            s = "Click me!"
    else:
        s = "Connecting..."
    text.set(s)

def got_focus(event):
    global has_focus
    has_focus = True
    update_text()

def lost_focus(event):
    global has_focus
    has_focus = False
    update_text()

root = Tk()
root.overrideredirect(1)  # Removes all window decorations!
frame = Frame(root, width=120, height=20)
frame.bind("<Key>", key)
frame.bind("<KeyRelease>", key_release)
frame.bind("<FocusIn>", got_focus)
frame.bind("<FocusOut>", lost_focus)
text = StringVar()
label = Label(frame, textvariable=text, bg="black", fg="green")
text.set("Connecting...")
label.pack()
frame.pack()
frame.focus_set()

class BgbThread(Thread):
    def run(self):
        import socket
        while True:
            try:
                bgb.connect()
                break
            except socket.error:
                pass
        global connected
        connected = True
        update_text()

bgb_thread = BgbThread()
bgb_thread.start()

root.mainloop()
