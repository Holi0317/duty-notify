#!/bin/bash

source env/bin/activate

./main.py || exit $?
