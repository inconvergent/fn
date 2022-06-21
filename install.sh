#!/bin/bash

mkdir -p ./dist
rm -rf ./dist/*
pip install wheel
python setup.py bdist_wheel
pip install `find dist -iname "fn*"`
