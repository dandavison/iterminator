import colorsys
import os
from plistlib import readPlist


class Scheme(object):
    """
    An iTerm2 color scheme.
    """
    def __init__(self, path):
        self.path = path
        self.name = os.path.basename(self.path).split('.')[0]
        self.scheme = self.parse_scheme()

    def background(self):
        background = self.scheme['Background Color']
        return (
            background['Red Component'],
            background['Green Component'],
            background['Blue Component'])

    def is_light(self):
        rgb = self.background()
        h, l, s = colorsys.rgb_to_hls(*rgb)
        return l >= 0.5

    def parse_scheme(self):
        return readPlist(self.path)

    def __repr__(self):
        return self.name
