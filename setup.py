#!/usr/bin/env python
# -*- coding: utf-8 -*-


try:
    from setuptools import setup, Command
except ImportError:
    from distutils.core import setup
from pip.req import parse_requirements


class PyTest(Command):
    user_options = []

    def initialize_options(self):
        import subprocess

        return_code = subprocess.call(
            ['pip', 'install', '-r' 'test-requirements.txt'])
        if return_code != 0:
            raise SystemExit(return_code)

    def finalize_options(self):
        pass

    def run(self):
        import sys, subprocess

        errno = subprocess.call([sys.executable, 'runtests.py'])
        raise SystemExit(errno)


readme = open('README.rst').read()
history = open('HISTORY.rst').read().replace('.. :changelog:', '')

requirements = [str(ir.req) for ir in parse_requirements('requirements.txt')]

test_requirements = [str(ir.req) for ir in
                     parse_requirements('test-requirements.txt')]

setup(
    name='rip',
    version='0.0.1',
    description='A python fframework for writing restful apis.',
    long_description=readme + '\n\n' + history,
    author='Aplopio developers',
    author_email='devs@aplopio.com',
    url='https://github.com/uttamk/rip',
    packages=[
        'rip',
    ],
    package_dir={'rip':
                     'rip'},
    include_package_data=True,
    install_requires=requirements,
    license="BSD",
    zip_safe=False,
    keywords='rip',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Natural Language :: English',
        "Programming Language :: Python :: 2",
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
    ],
    tests_require=test_requirements,
    cmdclass={'test': PyTest},
    test_suite='tests',
)
