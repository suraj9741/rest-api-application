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

## run new mogration 
flask db init
flask db migrate -m "Initial migration."
flask db upgrade

## Step 1: Clean DB state
DROP TABLE IF EXISTS alembic_version;
DROP TABLE IF EXISTS student;
## Step 2: Delete old migrations (already done by you)
rm -rf migrations
## Step 3: Reinitialize migrations
flask db init
## Step 4: Generate migration from models
flask db migrate -m "initial migration"
## Step 5: Apply migration
flask db upgrade
