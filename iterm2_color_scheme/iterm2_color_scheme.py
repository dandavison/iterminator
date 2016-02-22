#!/usr/bin/env python
from collections import namedtuple
from itertools import starmap
import collections
import logging
import os
import readline
import subprocess
import sys


logging.basicConfig(
    filename='/tmp/iterm2-color-scheme.log',
    level=logging.DEBUG,
)


class deque(collections.deque):
    def center(self, item):
        self.rotate(list(self).index(item))


class Scheme(namedtuple('Scheme', ['index', 'path'])):
    """
    An iTerm2 color scheme file.
    """
    @property
    def name(self):
        return os.path.basename(self.path).split('.')[0]

    def __repr__(self):
        return "%3d %s" % (self.index, self.name)


class ColorSchemeSelector(object):

    def __init__(self):
        self.repo_dir = os.path.join(os.path.dirname(__file__),
                                     'iTerm2-Color-Schemes')
        schemes_dir = self.repo_dir + '/schemes'
        self.schemes = deque(starmap(Scheme,
                                     enumerate(schemes_dir + '/' + f
                                               for f in os.listdir(schemes_dir)
                                               if f.endswith('.itermcolors'))))
        self.scheme = next(iter(self.schemes))

        self.name_to_scheme = {s.name: s for s in self.schemes}
        self.scheme_names = [s.name for s in self.schemes]
        readline.set_completer(self.complete)
        readline.set_completer_delims('')
        readline.parse_and_bind('tab: complete')
        readline.parse_and_bind('set completion-ignore-case on')
        readline.parse_and_bind('set completion-query-items -1')

    def select(self):
        """
        Select a color theme interactively.
        """
        if os.getenv('TMUX'):
            error("Please detach from your tmux session "
                  "before running this command.")

        while True:
            try:
                self.scheme = self.name_to_scheme[raw_input()]
            except KeyboardInterrupt:
                sys.stdout.write('\n')
                sys.exit(0)
            except KeyError:
                sys.exit(1)
            else:
                self.apply_scheme()

    def complete(self, text, state):
        response = None
        if state == 0:
            if text:
                self.current_matches = [s
                                for s in self.scheme_names
                                if s and text.lower() in s.lower()]
                logging.debug('%s current_matches: %s', repr(text), self.current_matches)
            else:
                self.current_matches = self.scheme_names
                logging.debug('(empty input) current_matches: %s', self.current_matches)

        try:
            response = self.current_matches[state]
        except IndexError:
            response = None
        else:
            if len(self.current_matches) == 1:
                self.apply_scheme(response)

        logging.debug('complete(%s, %s) => %s',
                      repr(text), state, repr(response))
        return response


    def apply_scheme(self, name=None):
        if name is not None:
            self.scheme = self.name_to_scheme[name]
        subprocess.check_call([
            self.repo_dir + '/tools/preview.rb',
            self.scheme.path,
        ])
        self.schemes.center(self.scheme)


def error(msg):
    print >>sys.stderr, msg
    exit(1)


def main():
    ColorSchemeSelector().select()


if __name__ == '__main__':
    main()
