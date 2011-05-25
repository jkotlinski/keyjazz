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

"""
Mapping of keyboard event to trashed PS/2 signal, as seen
by Game Boy.

These values do not directly correspond to what's in the
PS/2 standard. This is because Game Boy serial port does
not at all adhere to PS/2 standard, and the bytes
received are truncated. This also makes it impossible
to discern between certain keys, who happen to get the
same byte value after being truncated.

Example: Incoming byte 0xe0 is transfered backwards (I think),
loses some bits, and shows up as a 3... Makes sense? :)
"""

# Translates PC key event to messed up PS/2 keyboard signal,
# as is would be read on the Game Boy side.
def key_to_ps2(key):
    table = {
            # Single-byte keys.
            "Return": [0x2d],
            "Prior": [0x5f],  # Page up.
            "Next": [0x2f],  # Page down.
            "F1": [0x50],
            "F2": [0x30],
            "F3": [0x10],
            "F4": [0x18],
            "F5": [0x60],
            "F6": [0x68],
            "F8": [0x28],
            "F9": [0x40],
            "F10": [0x48],
            "F11": [0xf],
            "F12": [0x70],
            "space": [0x4a],
            "Home": [0x9b],
            "Insert": [7],
            "Delete": [0xc7],

            # Two-byte keys. First byte from PS/2 keyboard is originally 0xe0.
            "Down": [3, 0x27],
            "Up": [3, 0x57],
            "Right": [3, 0x17],
            "Left": [3, 0x6b]
            }
    try:
        return table[key]
    except KeyError:
        return []

def key_up_to_ps2(key):
    table = {
            "space": [0x80 | 0x4a],
            "F9": [0x80 | 0x40],
            "F10": [0x80 | 0x48],
            "F11": [0x80 | 0xf],
            "F12": [0x80 | 0x70],
            }
    try:
        return table[key]
    except KeyError:
        return []
