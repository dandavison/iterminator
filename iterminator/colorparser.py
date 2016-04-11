import colorsys
import os
from plistlib import readPlist


def parse_scheme(colorscheme_name):
        app_path = (os.path.abspath(os.path.dirname(__file__)) +
                    '/iTerm2-Color-Schemes/schemes/')
        colorscheme_path = app_path + colorscheme_name + '.itermcolors'
        config_path = os.path.abspath(colorscheme_path)

        config = readPlist(config_path)
        return config


def get_background(config):
    background = config['Background Color']
    return (
        background['Red Component'],
        background['Green Component'],
        background['Blue Component'])


def convert_background(r, g, b):
    return colorsys.rgb_to_hls(r, g, b)


def light_or_dark(colorscheme_name):
    colors = parse_scheme(colorscheme_name)
    rgb = get_background(colors)
    h, l, s = convert_background(*rgb)
    if l >= 0.5:
        return True
    return False
