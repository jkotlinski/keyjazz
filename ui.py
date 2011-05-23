from Tkinter import *

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
logo = Label(frame, text="Keyjazz!", bg="black", fg="green")
logo.pack()
frame.pack()
frame.focus_set()

root.mainloop()
