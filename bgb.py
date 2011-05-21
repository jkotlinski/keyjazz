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
CMD_JOYPAD = 101
CMD_SYNC_SEND = 104  # Sending byte as active.
CMD_SYNC_REPLY = 105 # Sending byte as passive.
CMD_SYNC_TICK = 106  # Sync only, no transfer.
CMD_LINKSPEED = 107
CMD_STATUS = 108

STATUS_ACTIVE = 1
STATUS_PAUSED = 3

def pack(ints):
    import struct
    return struct.pack("b" * len(ints), *ints)

def unpack(string):
    import struct
    return struct.unpack("b" * len(string), string)

def version():
    return pack([CMD_VERSION, 1, 3, 0])

import socket
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

def handle_reply():
    reply = s.recv(1024)
    while reply:
        cmd = ord(reply[0])
        if cmd == CMD_VERSION:
            version = unpack(reply[1:4])
            if version != (1, 3, 0):
                sys.exit("unknown BGB version", version)
            print "connected with BGB 1.3.0!"
        elif cmd == CMD_STATUS:
            status = ord(reply[1])
            if status == STATUS_ACTIVE:
                print "BGB active"
            elif status == STATUS_PAUSED:
                print "BGB paused"
            else:
                print "Unknown BGB status", status
        elif cmd == CMD_SYNC_TICK:
            pass
        else:
            print "Unknown command", cmd
            continue
        reply = reply[4:]


def connect():
    try:
        s.connect(("localhost", 8765))
    except socket.error:
        print "Connect failed!"
        return False
    s.send(pack([CMD_VERSION] + [1, 3, 0]))  # BGB v1.3.0
    handle_reply()
    s.send(pack([CMD_STATUS, STATUS_ACTIVE, 0, 0]))
    handle_reply()

J_START = 0x80
J_SELECT = 0x40
J_B = 0x20
J_A = 0x10
J_DOWN = 8
J_UP = 4
J_LEFT = 2
J_RIGHT = 1

connect()
while True:
    s.send(pack([CMD_JOYPAD, J_DOWN, 0, 0]))
    handle_reply()
