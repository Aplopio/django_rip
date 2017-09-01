#!/usr/bin/env python
# -*- coding: utf-8 -*-

try:
    from setuptools import setup, Command, find_packages
except ImportError:
    from distutils.core import setup
import pip
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

with open('requirements.txt') as f:
    requirements = [l.strip() for l in f.readlines()]

setup(
    name='django_rip',
    version='0.1.0',
    description='A python framework for writing restful APIs.',
    long_description=readme + '\n\n' + history,
    author='Aplopio developers',
    author_email='devs@aplopio.com',
    url='https://github.com/aplopio/django_rip',
    package_dir={'django_rip': 'django_rip'},
    packages=find_packages(),
    include_package_data=True,
    install_requires=[],
    license="MIT",
    zip_safe=False,
    keywords='rip, django_rip',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 2.7'
    ],
    cmdclass={'test': PyTest},
    test_suite='tests'
)
