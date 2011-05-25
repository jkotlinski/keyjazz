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

# Translates PC key event to messed up PS/2 keyboard signal,
# as is would be read on the Game Boy side.
def key_to_ps2(key):
    """
    These values do not directly correspond to what's in the
    PS/2 standard. This is because Game Boy serial port does
    not at all adhere to PS/2 standard, and the bytes
    received are truncated.

    Example: Incoming byte 0xe0 is transfered backwards (I think),
    loses some bits, and shows up as a 3... Makes sense? :)
    """
    table = {
            # Non-qualified keys.
            "Return": [0x2d],
            "Prior": [0x5f],  # Page up.
            "Next": [0x2f],  # Page down.

            # Extended keys. (First byte from PS/2 keyboard is 0xe0.)
            "Down": [3, 0x27],
            "Up": [3, 0x57],
            "Right": [3, 0x17],
            "Left": [3, 0x6b],
            }
    try:
        return table[key]
    except KeyError:
        return []
