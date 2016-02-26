import os

from setuptools import find_packages
from setuptools import setup


setup(
    name='iterm2-color-scheme',
    version=(open(os.path.join(os.path.dirname(__file__),
                               'iterm2_color_scheme',
                               'version.txt'))
             .read().strip()),
    author='Dan Davison',
    author_email='dandavison7@gmail.com',
    description="Command-line color scheme selector for iTerm2",
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    entry_points={
        'console_scripts': [
            'iterm2-color-scheme = iterm2_color_scheme.iterm2_color_scheme:main',
        ],
    },
)
