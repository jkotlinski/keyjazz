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

# BGB link protocol.

CMD_VERSION = 1
CMD_JOYPAD = 0x65
CMD_SYNC_SEND = 0x68  # Sending byte as active.
CMD_SYNC_REPLY = 0x69 # Sending byte as passive.
CMD_SYNC_TICK = 0x6a  # Sync only, no transfer.
CMD_LINKSPEED = 0x6b

def pack(ints):
    import struct
    return struct.pack("B" * len(ints), *ints)

def unpack(string):
    import struct
    return list(struct.unpack("B" * len(string), string))

def version():
    return pack([CMD_VERSION, 1, 3, 0])

import socket
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

def handle_reply():
    packet = s.recv(1024)
    while packet:
        cmd = ord(packet[0])
        if cmd == CMD_VERSION:
            reply = unpack(packet)
            version = reply[1:4]
            if version != [0, 0x55, 1]:
                sys.exit("wrong BGB version - use v1.12!")
            print "connected with BGB 1.12!"
            s.send(packet)
        elif cmd == CMD_SYNC_REPLY:
            # print "reply", unpack(packet)
            pass
        elif cmd == CMD_LINKSPEED:
            s.send(packet)
        elif cmd == CMD_JOYPAD:
            print "joypad", unpack(packet)
        elif cmd == CMD_SYNC_TICK:
            pass
            # print "tick", reply[2:4]
            # s.send(packet)
            # print time.time()
        else:
            print "Unknown command", cmd
            continue
        packet = packet[4:]

# May throw socket.error if connect times out.
def connect():
    s.connect(("localhost", 8765))
    handle_reply()

J_START = 0x80
J_SELECT = 0x40
J_B = 0x20
J_A = 0x10
J_DOWN = 8
J_UP = 4
J_LEFT = 2
J_RIGHT = 1

K_EXTENDED = 3

K_ENTER = 0x2d
K_UP = 0x57
K_DOWN = 0x27

def send(keys):
    s.setblocking(0)
    for key in keys:
        cmd = [CMD_SYNC_SEND, key, 0x85, 0]
        s.send(pack(cmd))
        # Since LSDj is rather timing specific, we need
        # to add some sleep here...
        import time
        time.sleep(0.03)

    try:
        handle_reply()
    except socket.error:
        pass
