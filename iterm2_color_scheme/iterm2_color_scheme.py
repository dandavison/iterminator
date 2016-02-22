#!/usr/bin/env python
import logging
import os
import readline
import subprocess
import sys


logging.basicConfig(
    filename='/tmp/iterm2-color-scheme.log',
    level=logging.DEBUG,
)


class Scheme(object):
    """
    An iTerm2 color scheme.
    """
    def __init__(self, path):
        self.path = path

    @property
    def name(self):
        return os.path.basename(self.path).split('.')[0]

    def __repr__(self):
        return self.name


class ColorSchemeSelector(object):
    """
    An interactive iTerm2 color scheme selector.
    """

    def __init__(self):
        self.repo_dir = os.path.join(os.path.dirname(__file__),
                                     'iTerm2-Color-Schemes')
        schemes_dir = self.repo_dir + '/schemes'
        self.schemes = [
            Scheme(os.path.join(schemes_dir, scheme_file))
            for scheme_file in os.listdir(schemes_dir)
            if scheme_file.endswith('.itermcolors')
        ]

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
        """
        Return state'th completion for current input.

        This is the standard readline completion function.
        https://docs.python.org/2/library/readline.html

        text: the current input
        state: an integer specifying which of the matches for the current input
               should be returned
        """
        if state == 0:
            # First call for current input; compute and cache completions
            if text:
                self.current_matches = self.get_matches(text)
                logging.debug('%s current_matches: %s', repr(text), self.current_matches)

                if len(self.current_matches) == 1:
                    # Unique match; apply scheme and return the completion
                    [completion] = self.current_matches
                    self.apply_scheme(completion)
                    return completion
            else:
                self.current_matches = self.scheme_names
                logging.debug('(empty input) current_matches: %s', self.current_matches)
        try:
            completion = self.current_matches[state]
        except IndexError:
            completion = None

        logging.debug('complete(%s, %s) => %s',
                      repr(text), state, repr(completion))
        return completion

    def get_matches(self, text):
        """
        Return matches for current readline input.
        """
        return [
            name
            for name in self.scheme_names
            if text.lower() in name.lower()
        ]

    def apply_scheme(self, name=None):
        """
        Apply current scheme to current iTerm2 session.
        """
        if name is not None:
            self.scheme = self.name_to_scheme[name]
        subprocess.check_call([
            self.repo_dir + '/tools/preview.rb',
            self.scheme.path,
        ])


def error(msg):
    print >>sys.stderr, msg
    exit(1)


def main():
    ColorSchemeSelector().select()


if __name__ == '__main__':
    main()
