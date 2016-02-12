#!/usr/bin/env python
import os
import random
import subprocess
import sys
import termios
import tty


def error(msg):
    print >>sys.stderr, msg
    exit(1)


def warn(msg):
    print >>sys.stderr, msg


class ColorSchemeChooser(object):
    JUMP = {':', '/'}
    NEXT = {'j'}
    PREV = {'k'}

    def __init__(self):
        ics_repo = os.path.join(os.path.dirname(__file__),
                                'iTerm2-Color-Schemes')
        self.schemes_dir = ics_repo + '/schemes'
        self.apply_script = ics_repo + '/tools/preview.rb'
        self.schemes = os.listdir(self.schemes_dir)
        self.blank = ' ' * max(len(s) for s in self.schemes)

    def run(self):
        if os.getenv('TMUX'):
            error("Please detach from your tmux session "
                  "before running this script.")

        self.print_usage()

        i = random.choice(range(len(self.schemes)))
        while True:
            key = read_character()
            if key in self.NEXT:
                i += 1
            elif key in self.PREV:
                i -= 1
            elif key in self.JUMP:
                self.print_msg('')
                cmd = raw_input(':')
                try:
                    i = int(cmd)
                except ValueError:
                    try:
                        i = next(i for i, scheme in enumerate(self.schemes)
                                 if cmd.lower() in scheme.lower())
                    except StopIteration:
                        self.print_usage()
                        continue
            else:
                print
                exit(0)
            i = i % len(self.schemes)
            self.apply_scheme(i)
            self.print_scheme(i)

    def apply_scheme(self, i):
        scheme = self.schemes[i]
        subprocess.check_call([
            self.apply_script,
            self.schemes_dir + '/' + scheme,
        ])

    def print_msg(self, msg):
        sys.stdout.write("\r%s\r%s" % (self.blank, msg))

    def print_scheme(self, i):
        scheme_name = self.schemes[i].split('.')[0]
        self.print_msg("%3d %s" % (i, scheme_name))

    def print_usage(self):

        def format_set(s):
            return  '{%s}' % ','.join(sorted(s))

        print '{next}/{prev} to navigate, {jump} to jump'.format(
            next=format_set(self.NEXT),
            prev=format_set(self.PREV),
            jump=format_set(self.JUMP),
        ),


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


def main():
    ColorSchemeChooser().run()


if __name__ == '__main__':
    main()
