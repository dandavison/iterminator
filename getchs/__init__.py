from select import select
from sys import stdin
from time import sleep
import fcntl
import os
import termios
import tty


POLL_INTERVAL = 0.1

CTRL_C = "\x03"
LEFT = "\x1b[D"
RIGHT = "\x1b[C"
UP = "\x1b[A"
DOWN = "\x1b[B"


def setNonBlocking(fd):
    """
    Set the file description of the given file descriptor to non-blocking.

    Copied from twisted.internet.fdesc.setNonBlocking()
    https://github.com/twisted/twisted
    """
    flags = fcntl.fcntl(fd, fcntl.F_GETFL)
    flags = flags | os.O_NONBLOCK
    fcntl.fcntl(fd, fcntl.F_SETFL, flags)


def getchs():
    """
    Block until there are bytes to read on stdin and then return them all.

    Adapted from getch()
    https://github.com/joeyespo/py-getch.
    """
    fd = stdin.fileno()
    old = termios.tcgetattr(fd)
    setNonBlocking(fd)
    try:
        tty.setraw(fd)
        while not select([stdin], [], [], 0)[0]:
            sleep(POLL_INTERVAL)
        return stdin.read()
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old)


if __name__ == "__main__":
    while True:
        chars = getchs()
        if chars == CTRL_C:
            exit(0)
        else:
            print("%r" % chars, map(ord, chars))
