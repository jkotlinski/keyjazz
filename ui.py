"""
Copyright (c) 2011, Johan Kotlinski

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.
"""

from Tkinter import *
from threading import Thread
import Queue

import bgb
import ps2

connected = False

send_queue = Queue.Queue()

# UI callbacks.
def key(event):
    cmd = ps2.key_to_ps2(event.keysym)
    if cmd:
        send_queue.put(cmd)
    else:
        print "unknown key", event.keysym

def key_release(event):
    cmd = ps2.key_up_to_ps2(event.keysym)
    if cmd:
        send_queue.put(cmd)
    else:
        pass

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

def destroy(event=None):
    global connected
    connected = True
    send_queue.put(None)

# Init UI.
root = Tk()
root.title("Keyjazz")
root.bind("<Destroy>", destroy)
frame = Frame(root)
frame.bind("<Key>", key)
frame.bind("<KeyRelease>", key_release)
frame.bind("<FocusIn>", got_focus)
frame.bind("<FocusOut>", lost_focus)
text = StringVar()
label = Label(frame, width=20, height=4,
        textvariable=text, bg="black", fg="green")
text.set("Connecting...")
label.pack()
frame.pack()
frame.focus_set()

# Init BGB link.
class BgbThread(Thread):
    def run(self):
        import socket
        global connected
        while not connected:
            try:
                bgb.connect()
                connected = True
            except socket.error:
                pass
        update_text()

        while True:
            cmd = send_queue.get()
            if not cmd:
                break
            bgb.send(cmd)

BgbThread().start()

try:
    root.mainloop()
except KeyboardInterrupt:
    destroy()
