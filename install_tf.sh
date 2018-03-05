#!/bin/bash
# Install tensorflow on Mac if pip3 install throws a hissy fit

# Yes I realize this is rather inconvenient to maintain but tensorflow is
# messing the entire installation on some virtual machines
pip3 install https://storage.googleapis.com/tensorflow/mac/cpu/tensorflow-1.6.0-py3-none-any.whl

