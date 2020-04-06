#!/bin/bash

. $PWD/venv/bin/activate

echo $PATH

cd src

echo $PWD

python track_changes.py