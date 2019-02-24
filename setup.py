#!/usr/bin/env python3
# -*- coding: utf-8 -*-


try:
  from setuptools import setup
except ImportError:
  from distutils.core import setup


setup(name='fn',
      version='1.1.0',
      description='fn',
      url='',
      license='MIT License',
      author='Anders Hoff',
      author_email='inconvergent@gmail.com',
      install_requires=['docopt', 'gitpython'],
      packages=['fn'],
      entry_points={'console_scripts': ['fn=fn:run']},
      zip_safe=True,
      )

