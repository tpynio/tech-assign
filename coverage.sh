#!/bin/bash

export TESTING=1
export ENV_FILE=/Users/ivan/Project/tech-assign/backend/.env

coverage run --source=backend --omit=backend/tests/* -m pytest backend/tests

coverage report -m

coverage html
