#!/usr/bin/env python
import argparse
import os
import readline
import subprocess
import sys


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

                if len(self.current_matches) == 1:
                    # Unique match; apply scheme and return the completion
                    [completion] = self.current_matches
                    self.apply_scheme(completion)
                    return completion
            else:
                self.current_matches = self.scheme_names
        try:
            completion = self.current_matches[state]
        except IndexError:
            completion = None

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


def main():
    if os.getenv('TMUX'):
        print >>sys.stderr, (
            "Please detach from your tmux session before running this command."
        )
        sys.exit(1)

    selector = ColorSchemeSelector()
    padding = ' ' * 100
    arg_parser = argparse.ArgumentParser(
        description=("Color theme selector for iTerm2. Use TAB to complete "
                     "color scheme names, or supply one of the command-line "
                     "arguments."),
        epilog=(
            "The color schemes are from "
            "https://github.com/mbadolato/iTerm2-Color-Schemes, which is "
            "included as a git submodule in this project. All credit for the "
            "schemes goes to the original scheme authors and to the "
            "iTerm2-Color-Schemes project. To add a new scheme, please first "
            "create a pull request against iTerm2-Color-Schemes to add your "
            "scheme, and then open a pull request or issue against "
            "https://github.com/dandavison/iterm2-color-scheme to update the "
            "submodule."),
        formatter_class=argparse.RawTextHelpFormatter,
    )

    arg_parser.add_argument(
        '-l', '--list', action='store_true',
        help="List available color schemes",
    )

    arg_parser.add_argument(
        '--scheme',
        metavar='scheme',
        help="Available choices are\n%s" % ' | '.join(selector.scheme_names),
    )

    args = arg_parser.parse_args()

    if args.list:
        for name in selector.scheme_names:
            print name
    elif args.scheme:
        selector.apply_scheme(args.scheme)
    else:
        selector.select()


if __name__ == '__main__':
    main()
