#!/usr/bin/env python3
# -*- coding: utf-8 -*-

try:
  from setuptools import setup
except ImportError:
  from distutils.core import setup

dependencies = [
    'docopt',
    'gitpython'
    ]

setup(
    name='fn',
    version='0.2.0',
    description='fn',
    url='',
    license='MIT License',
    author='Anders Hoff',
    author_email='inconvergent@gmail.com',
    install_requires=dependencies,
    packages=[
        'fn'
        ],
    entry_points={
        'console_scripts': [
            'fn=fn:run'
            ]
        },
    zip_safe=True
    )

