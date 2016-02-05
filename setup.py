# -*- coding: utf-8 -*-

"""LLVM Blitz3d implementation

Read the doc: <https://github.com/vslutov/llb3d>
"""

from setuptools import setup, find_packages

VERSION = "0.0.1" # Don't forget fix in __main__.py

setup(name='llb3d',
      version=VERSION,
      description=__doc__,
      maintainer='vslutov',
      maintainer_email='vslutov@yandex.ru',
      url='https://github.com/vslutov/llb3d',
      license='WTFPL',
      platforms=['any'],
      classifiers=["Development Status :: 1 - Planning",
                   "Environment :: Console",
                   "Environment :: X11 Applications",
                   "Intended Audience :: Education",
                   "Intended Audience :: Developers",
                   "Natural Language :: Russian",
                   "Natural Language :: English",
                   "Operating System :: OS Independent",
                   "Programming Language :: Python :: 3 :: Only",
                   "Topic :: Games/Entertainment",
                   "Topic :: Software Development :: Compilers",
                   "Topic :: Software Development :: Libraries"],
      install_requires=['pytest'],
      packages=find_packages(),
      include_package_data=True,
      entry_points={'console_scripts': ['llb3d = llb3d.__main__:main']})
