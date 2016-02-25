from setuptools import find_packages
from setuptools import setup

from iterm2_color_scheme.iterm2_color_scheme import __version__


setup(
    name='iterm2-color-scheme',
    version=__version__,
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
    install_requires = [
        'py-getch',
    ],
)
