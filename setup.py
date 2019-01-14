#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""LLVM Blitz3d implementation.

Read the doc: <https://github.com/vslutov/llb3d>
"""

import os
import sys
import subprocess
import textwrap
import pathlib

from setuptools import setup, find_packages, Extension
from setuptools.command.build_ext import build_ext as build_ext_orig

DOCLINES = (__doc__ or '').split("\n")

PROJECT             = 'llb3d'
MAJOR               = 0
MINOR               = 0
PATCH               = 3
ISRELEASED          = os.environ.get('TRAVIS_BUILD_STAGE_NAME') == 'Deploy'
VERSION             = '%d.%d.%d' % (MAJOR, MINOR, PATCH)

# Return the git revision as a string
def git_version():
    def _minimal_ext_cmd(cmd):
        # construct minimal environment
        env = {}
        for k in ['SYSTEMROOT', 'PATH', 'HOME']:
            v = os.environ.get(k)
            if v is not None:
                env[k] = v
        # LANGUAGE is used on win32
        env['LANGUAGE'] = 'C'
        env['LANG'] = 'C'
        env['LC_ALL'] = 'C'
        out = subprocess.Popen(cmd, stdout=subprocess.PIPE, env=env).communicate()[0]
        return out

    try:
        out = _minimal_ext_cmd(['git', 'rev-parse', 'HEAD'])
        GIT_REVISION = out.strip().decode('ascii')
    except OSError:
        GIT_REVISION = "Unknown"

    return GIT_REVISION

def get_version_info():
    # Adding the git rev number needs to be done inside write_version_py(),
    # otherwise the import of numpy.version messes up the build under Python 3.
    FULLVERSION = VERSION
    if os.path.exists('.git'):
        GIT_REVISION = git_version()
    else:
        GIT_REVISION = "Unknown"

    if not ISRELEASED:
        FULLVERSION += '.dev0+' + GIT_REVISION[:7]

    return FULLVERSION, GIT_REVISION


def write_version_py(filename='{name}/version.py'.format(name=PROJECT)):
    cnt = """\"\"\"LLB3D version.\"\"\"

SHORT_VERSION = '{version}'
VERSION = '{version}'
FULL_VERSION = '{full_version}'
GIT_REVISION = '{git_revision}'
RELEASE = {isrelease}

if not RELEASE:
    VERSION = FULL_VERSION
"""
    FULLVERSION, GIT_REVISION = get_version_info()

    a = open(filename, 'w')
    try:
        a.write(cnt.format(version=VERSION,
                           full_version=FULLVERSION,
                           git_revision=GIT_REVISION,
                           isrelease=str(ISRELEASED)))
    finally:
        a.close()

class CMakeExtension(Extension):

    def __init__(self, name):
        # don't invoke the original build_ext for this special extension
        super().__init__(name, sources=[])

class build_ext(build_ext_orig):

    def run(self):
        for ext in self.extensions:
            self.build_cmake(ext)

    def build_cmake(self, ext):
        cwd = pathlib.Path().absolute()

        # these dirs will be created in build_py, so if you don't have
        # any python sources to bundle, the dirs will be missing
        build_temp = pathlib.Path(self.build_temp)
        build_temp.mkdir(parents=True, exist_ok=True)
        extdir = pathlib.Path(self.get_ext_fullpath(ext.name))

        # cmake args
        BBPROGRAM_SOURCE = str(extdir.parent.absolute() / PROJECT / 'bbprogram')
        config = 'Debug' if self.debug else 'Release'
        cmake_args = [
            '-DCMAKE_ARCHIVE_OUTPUT_DIRECTORY=' + BBPROGRAM_SOURCE,
            '-DCMAKE_LIBRARY_OUTPUT_DIRECTORY=' + BBPROGRAM_SOURCE,
            '-DCMAKE_RUNTIME_OUTPUT_DIRECTORY=' + BBPROGRAM_SOURCE,
            '-DCMAKE_BUILD_TYPE=' + config
        ]

        # build args
        build_args = [
            '--config', config
        ]

        os.chdir(str(build_temp))
        self.spawn(['cmake', str(cwd / PROJECT / ext.name)] + cmake_args)
        if not self.dry_run:
            self.spawn(['cmake', '--build', '.'] + build_args)
        os.chdir(str(cwd))

def setup_package():
    src_path = os.path.dirname(os.path.abspath(sys.argv[0]))
    old_path = os.getcwd()
    os.chdir(src_path)
    sys.path.insert(0, src_path)

    # Rewrite the version file everytime
    write_version_py()

    metadata = dict(
        name = PROJECT,
        maintainer = "vslutov",
        maintainer_email = "vslutov@yandex.ru",
        description = DOCLINES[0],
        long_description = "\n".join(DOCLINES[2:]),
        url = "https://github.com/vslutov/llb3d",
        download_url = "https://pypi.python.org/pypi/llb3d",
        license = 'WTFPL',
        classifiers=["Development Status :: 1 - Planning",
                     "Environment :: Console",
                     "Environment :: X11 Applications",
                     "Intended Audience :: Developers",
                     "Natural Language :: English",
                     "Operating System :: OS Independent",
                     "Programming Language :: Python :: 3 :: Only",
                     "Topic :: Games/Entertainment",
                     "Topic :: Software Development :: Compilers",
                     "Topic :: Software Development :: Libraries",
                     "License :: OSI Approved :: GNU Affero General Public License v3 or later (AGPLv3+)"],
        platforms = ['any'],
        install_requires=['pytest>=3.7',
                          'ply>=3.11',
                          'llvmlite>=0.24',
                          'typeguard>=2.2.2',
                          'wheel>=0.31.1'],
        extras_require={
          'dev': [
              'pytest>=3.7',
              'pytest-cov>=2.5',
              'pylint>=2.1'
          ]
        },
        packages=find_packages(),
        entry_points={'console_scripts': ['{name} = {name}.__main__:main'.format(name=PROJECT)]},
        version=get_version_info()[0],
        zip_safe=False,
        ext_modules=[CMakeExtension('bbruntime')],
        cmdclass={
            'build_ext': build_ext,
        }
    )

    try:
        setup(**metadata)
    finally:
        del sys.path[0]
        os.chdir(old_path)
    return

if __name__ == "__main__":
    setup_package()
