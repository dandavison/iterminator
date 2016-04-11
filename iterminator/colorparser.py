import colorsys
import json
import os
import ConfigParser


def get_config(colorscheme_name):
        app_path = os.path.abspath(os.path.dirname(__file__)) + '/iTerm2-Color-Schemes/konsole/'
        colorscheme_path = app_path + colorscheme_name + '.colorscheme'
        config_path = os.path.abspath(colorscheme_path)

        config = ConfigParser.ConfigParser()
        config.read(config_path)
        return config


def get_background(config):
    background = [int(x) for x in config.get('Background', 'Color').split(',')]
    return tuple(background)


def convert_background(r, g, b):
    return colorsys.rgb_to_hls(r, g, b)

if __name__ == '__main__':
    config = get_config(colorscheme_name='Spring')


for scheme in LIGHT_SCHEMES:
    config = get_config(scheme)
    try:
        background = get_background(config)
    except:
        import ipdb; ipdb.set_trace()
    hls = convert_background(*background)
    print hls
