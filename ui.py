from Tkinter import *
from threading import Thread

import bgb

def key(event):
    print "pressed", event.keysym

def key_release(event):
    print "release", event.keysym

root = Tk()
root.title("Keyjazz")
root.overrideredirect(1)  # Removes all window decorations!
frame = Frame(root, width=120, height=20)
frame.bind("<Key>", key)
frame.bind("<KeyRelease>", key_release)
text = StringVar()
text.set("Connecting...")
logo = Label(frame, textvariable=text, bg="black", fg="green")
logo.pack()
frame.pack()
frame.focus_set()

class BgbThread(Thread):
    def run(self):
        import socket
        try:
            bgb.connect()
        except socket.error:
            text.set("Connect failed!")
            import time
            time.sleep(2)
            root.destroy()
        text.set("Keyjazz!")

bgb_thread = BgbThread()
bgb_thread.start()

root.mainloop()
