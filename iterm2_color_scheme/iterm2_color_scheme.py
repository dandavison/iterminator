#!/usr/bin/env python
from collections import deque
from collections import namedtuple
from itertools import chain
from itertools import starmap
import os
import subprocess
import sys
import termios
import tty


UP_ARROW = '\x1b[A'


class Scheme(namedtuple('Scheme', ['index', 'path'])):
    """
    An iTerm2 color scheme file.
    """
    @property
    def name(self):
        return os.path.basename(self.path).split('.')[0]

    def __repr__(self):
        return "%3d %s" % (self.index, self.name)


class ColorSchemeBrowser(object):
    JUMP_TO_NAME = {'/'}
    JUMP_TO_POSITION = {':'}
    NEXT = {'j'}
    PREV = {'k'}

    def __init__(self):
        self.repo_dir = os.path.join(os.path.dirname(__file__),
                                     'iTerm2-Color-Schemes')
        schemes_dir = self.repo_dir + '/schemes'
        self.schemes = deque(starmap(Scheme,
                                     enumerate(schemes_dir + '/' + f
                                               for f in os.listdir(schemes_dir)
                                               if f.endswith('.itermcolors'))))

        # A blank string that is long enough to conceal all other output
        self.blank = ' ' * max(chain((len(repr(s)) for s in self.schemes),
                                     [len(self.usage)]))

    @property
    def scheme(self):
        return self.schemes[0]

    def browse(self):
        """
        Select a color theme interactively.
        """
        if os.getenv('TMUX'):
            error("Please detach from your tmux session "
                  "before running this script.")

        self.display(self.usage)

        prev_pattern = None
        while True:
            key = read_character()
            if key in self.NEXT:
                self.next_scheme()
            elif key in self.PREV:
                self.prev_scheme()
            elif key in self.JUMP_TO_POSITION:
                self.display('')
                pattern = raw_input(':')

                if pattern == UP_ARROW:
                   if prev_pattern:
                       pattern = prev_pattern
                   else:
                       self.display(self.usage)
                       continue
                else:
                    prev_pattern = pattern

                try:
                    self.jump_to_position(int(pattern))
                except ValueError:
                    self.display(self.usage)
                    continue
            elif key in self.JUMP_TO_NAME:
                self.display('')
                pattern = raw_input('/')

                if pattern == UP_ARROW:
                   if prev_pattern:
                       pattern = prev_pattern
                   else:
                       self.display(self.usage)
                       continue
                else:
                    prev_pattern = pattern

                try:
                    self.jump_to_name(pattern)
                except StopIteration:
                    self.display(self.usage)
                    continue
            else:
                exit(0)
            self.apply_scheme()
            self.display(self.scheme)

    def next_scheme(self):
        self.schemes.rotate(-1)

    def prev_scheme(self):
        self.schemes.rotate(+1)

    def jump_to_position(self, i):
        self.schemes.rotate(self.scheme.index - i)

    def jump_to_name(self, pattern):
        pattern = pattern.lower()
        initial_scheme = self.scheme
        self.next_scheme()
        while pattern not in self.scheme.name.lower():
            if self.scheme == initial_scheme:
                raise StopIteration
            self.next_scheme()

    def apply_scheme(self):
        subprocess.check_call([
            self.repo_dir + '/tools/preview.rb',
            self.scheme.path,
        ])

    def display(self, string):
        """
        Display a string, overwriting previous content.
        """
        sys.stdout.write("\r%s\r%s" % (self.blank, string))

    @property
    def usage(self):
        def format_set(s):
            return  ''.join(sorted(s))

        return '{nextprev} to navigate, {jump} to jump'.format(
            nextprev=format_set(self.NEXT | self.PREV),
            jump=format_set(self.JUMP_TO_NAME | self.JUMP_TO_POSITION),
        )


def read_character():
    """
    http://stackoverflow.com/questions/510357/python-read-a-single-character-from-the-user
    """
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    try:
        tty.setraw(sys.stdin.fileno())
        return sys.stdin.read(1)
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)


def error(msg):
    print >>sys.stderr, msg
    exit(1)


def warn(msg):
    print >>sys.stderr, msg


def main():
    ColorSchemeBrowser().browse()


if __name__ == '__main__':
    main()
