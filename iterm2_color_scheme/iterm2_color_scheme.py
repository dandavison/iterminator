#!/usr/bin/env python
from collections import namedtuple
from itertools import starmap
import logging
import os
import readline
import subprocess
import sys


logging.basicConfig(
    filename='/tmp/iterm2-color-scheme.log',
    level=logging.DEBUG,
)


class SimpleCompleter(object):

    def __init__(self, options):
        self.options = sorted(options)
        return

    def complete(self, text, state):
        response = None
        if state == 0:
            # This is the first time for this text, so build a match list.
            if text:
                self.matches = [s
                                for s in self.options
                                if s and text.lower() in s.lower()]
                logging.debug('%s matches: %s', repr(text), self.matches)
            else:
                self.matches = self.options[:]
                logging.debug('(empty input) matches: %s', self.matches)

        # Return the state'th item from the match list,
        # if we have that many.
        try:
            response = self.matches[state]
        except IndexError:
            response = None
        logging.debug('complete(%s, %s) => %s',
                      repr(text), state, repr(response))
        return response


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

    def __init__(self):
        self.repo_dir = os.path.join(os.path.dirname(__file__),
                                     'iTerm2-Color-Schemes')
        schemes_dir = self.repo_dir + '/schemes'
        self.schemes = {
            s.name: s
            for s in starmap(Scheme,
                             enumerate(schemes_dir + '/' + f
                                       for f in os.listdir(schemes_dir)
                                       if f.endswith('.itermcolors')))
        }
        readline.set_completer(
            SimpleCompleter(s.name for s in self.schemes.values())
            .complete)
        readline.set_completer_delims('')
        readline.parse_and_bind('tab: menu-complete')

    def browse(self):
        """
        Select a color theme interactively.
        """
        if os.getenv('TMUX'):
            error("Please detach from your tmux session "
                  "before running this script.")

        while True:
            self.scheme = self.schemes[raw_input()]
            self.apply_scheme()

    def apply_scheme(self):
        subprocess.check_call([
            self.repo_dir + '/tools/preview.rb',
            self.scheme.path,
        ])


def error(msg):
    print >>sys.stderr, msg
    exit(1)


def main():
    ColorSchemeBrowser().browse()


if __name__ == '__main__':
    main()
