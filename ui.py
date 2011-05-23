from Tkinter import *

def key(event):
    print "pressed", event.keysym

def key_release(event):
    print "release", event.keysym

root = Tk()
frame = Frame(root, height=80)
frame.bind("<Key>", key)
frame.bind("<KeyRelease>", key_release)
frame.pack()
frame.focus_set()

root.mainloop()
