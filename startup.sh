#!/bin/bash

## start postgress contaner
##docker compose -f postgres.yaml up -d 

## create virtual environment and activate it 

##python3 -m venv /Users/one2n/py_env/student 

source /Users/one2n/py_env/student/bin/activate

## run application
python run.py 

## run test cases
PYTHONPATH=. pytest