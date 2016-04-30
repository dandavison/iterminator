import colorsys
import os
from plistlib import readPlist


def get_background(config):
    background = config['Background Color']
    return (
        background['Red Component'],
        background['Green Component'],
        background['Blue Component'])


def convert_background(r, g, b):
    return colorsys.rgb_to_hls(r, g, b)


class Scheme(object):
    """
    An iTerm2 color scheme.
    """
    def __init__(self, path):
        self.path = path
        self.name = os.path.basename(self.path).split('.')[0]
        self.scheme = self.parse_scheme()

    def is_light(self):
        rgb = get_background(self.scheme)
        h, l, s = convert_background(*rgb)
        return l >= 0.5

    def parse_scheme(self):
        return readPlist(self.path)

    def __repr__(self):
        return self.name
