import os

from setuptools import find_packages
from setuptools import setup


setup(
    name="iterminator",
    version=(
        open(os.path.join(os.path.dirname(__file__), "iterminator", "version.txt")).read().strip()
    ),
    author="Dan Davison",
    author_email="dandavison7@gmail.com",
    description="Command-line color scheme selector for iTerm2",
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=["gnureadline>=8.0.0"],
    entry_points={"console_scripts": ["iterminator = iterminator.iterminator:main"]},
)
