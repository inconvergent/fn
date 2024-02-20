#!/usr/bin/env python3.11


try:
  from setuptools import setup
except ImportError:
  from distutils.core import setup


setup(name='fn',
      version='2.4.0',
      description='fn',
      url='https://github.com/inconvergent/fn',
      license='MIT License',
      author='Anders Hoff',
      author_email='inconvergent@gmail.com',
      install_requires=['docopt'],
      packages=['fn'],
      entry_points={'console_scripts': ['fn=fn:main']},
      zip_safe=True,
      )

