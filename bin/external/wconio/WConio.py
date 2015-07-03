#!/usr/bin/env python
"""WConio.py -- Windows Console I/O Module

The _WConio.pyd module is based on TCCONIO; the comment from the original
source file is below:

    Old Turbo-C CONIO.H compatibility library for LCC-Win32
    and GCC/EGCS Mingw32 compilers.
    Version 1.0 (September 1999).
    Created by Daniel Guerrero Miralles (daguer@geocities.com).
    This source code is public domain.

Most functions are implemented in C due to lack of needed calls in the win32*
packages (most console functions seem to be missing).  A few were easier to
build in Python; you'll find them below.

This is strictly an ASCII module; I have no need of UNICODE for my projects and
honestly don't understand it well enough anyway.  Patches are welcome!
"""

__version__ = "1.5"

from _WConio import *


BLACK = 0
BLUE = 1
GREEN = 2
CYAN = 3
RED = 4
MAGENTA = 5
BROWN = 6
LIGHTGRAY = LIGHTGREY = 7
DARKGRAY = DARKGREY = 8
LIGHTBLUE = 9
LIGHTGREEN = 10
LIGHTCYAN = 11
LIGHTRED = 12
LIGHTMAGENTA = 13
YELLOW = 14
WHITE = 15

__keydict = {
    0x3b : 'f1',
    0x3c : 'f2',
    0x3d : 'f3',
    0x3e : 'f4',
    0x3f : 'f5',
    0x40 : 'f6',
    0x41 : 'f7',
    0x42 : 'f8',
    0x43 : 'f9',
    0x44 : 'f10',

    0x68 : 'altf1',
    0x69 : 'altf2',
    0x6a : 'altf3',
    0x6b : 'altf4',
    0x6c : 'altf5',
    0x6d : 'altf6',
    0x6e : 'altf7',
    0x6f : 'altf8',
    0x70 : 'altf9',
    0x71 : 'altf10',

    0x5e : 'ctrlf1',
    0x5f : 'ctrlf2',
    0x60 : 'ctrlf3',
    0x61 : 'ctrlf4',
    0x62 : 'ctrlf5',
    0x63 : 'ctrlf6',
    0x64 : 'ctrlf7',
    0x65 : 'ctrlf8',
    0x66 : 'ctrlf9',
    0x67 : 'ctrlf10',

    0x54 : 'shiftf1',
    0x55 : 'shiftf2',
    0x56 : 'shiftf3',
    0x57 : 'shiftf4',
    0x58 : 'shiftf5',
    0x59 : 'shiftf6',
    0x5a : 'shiftf7',
    0x5b : 'shiftf8',
    0x5c : 'shiftf9',
    0x5d : 'shiftf10',

    0x52 : 'ins',
    0x53 : 'del',
    0x4f : 'end',
    0x50 : 'down',
    0x51 : 'pgdn',
    0x4b : 'left',
    0x4d : 'right',
    0x47 : 'home',
    0x48 : 'up',
    0x49 : 'pgup',

    0xa2 : 'altins',
    0xa3 : 'altdel',
    0x9f : 'altend',
    0xa0 : 'altdown',
    0xa1 : 'altpgdn',
    0x9b : 'altleft',
    0x9d : 'altright',
    0x97 : 'althome',
    0x98 : 'altup',
    0x99 : 'altpgup',

    0x92 : 'ctrlins',
    0x93 : 'ctrldel',
    0x75 : 'ctrlend',
    0x91 : 'ctrldown',
    0x76 : 'ctrlpgdn',
    0x73 : 'ctrlleft',
    0x74 : 'ctrlright',
    0x77 : 'ctrlhome',
    0x8d : 'ctrlup',
    0x84 : 'ctrlpgup',

    3 : 'ctrl2'
}

def cputs(s):
    for c in s:
        putch(c)

def getkey():
    n, c = getch()
    # 0340 is 'grey' keys.  change this if you don't like 
    # it, but I don't care what color the key is.  IMHO it
    # just confuses the end-user if they need to know.
    if n == 0 or n == 0340:
        n, c = getch()
        if __keydict.has_key(n):
            return __keydict[n]
        return "key%x" % n
    return c

def cgets(l):
    s = ""
    c = getkey()
    while c != '\n' and c != '\r':
        if c == '\010': # backspace
            if s:
                s = s[:-1]
                gotoxy(wherex() - 1, wherey())
                putch(" ")
                gotoxy(wherex() - 1, wherey())
        elif c >= " " and c <= "~":
            if len(s) < l:
                s = s + c
                putch(c)
        c = getkey()
    return s

def textmode():
    textattr(LIGHTGRAY)
    clrscr()
    setcursortype(1)

def textcolor(c):
    bgcolor = gettextinfo()[4] & 0x00F0
    textattr(c | bgcolor)

def textbackground(c):
    fgcolor = gettextinfo()[4] & 0x000F
    textattr((c << 4) | fgcolor)

def getche():
    rc, s = getch()
    if s:
        putch(s)
    return (rc, s)

def normvideo():
    textattr(gettextinfo()[5])

def movetext(left, top, right, bottom, destleft, desttop):
    s = gettext(left, top, right, bottom)
    puttext(destleft, desttop, 
        right + (destleft - left), 
        bottom + (desttop - top), s)

class WCFile:
    def __init__(self):
        self.closed = 0
        self.mode = "r+"
        self.name = "<WConio>"
        self.softspace = 0
    def close(self):
        pass
    def flush(self):
        pass
    def isatty(self):
        return 1
    def read(self, size = 1):
        if size <= 1:
            return getch()[1]
        else:
            return cgets(size)
    def readline(self, size = 0):
        rc = cgets(size)
        if size:
            rc = rc[:size]
        return rc
    def readlines(self, sizehint = 0):
        "readlines() is pure nonsense for WConio, so this just calls readline."
        return readline(self, sizehint)
    def write(self, str):
        cputs(str)
    def writelines(self, l):
        for i in l:
            cputs(i)

File = WCFile()     # we just keep one of these around,
del WCFile          # so the class gets used just once.

if __name__ == '__main__':
    c = getkey()
    while c != '\n' and c != '\r':
        print `c`
        c = getkey()

# end of file.
