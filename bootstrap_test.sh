#!/bin/bash

sudo apt install virtualenv python3-pip

rm test_env -rf
virtualenv test_env --python=python3
. test_env/bin/activate
pip install -r test-requirements.txt
