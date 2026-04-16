#!/bin/bash
EXECUTABLE_NAME=hello_world
python3 /apps/${EXECUTABLE_NAME}.py > /tmp/${EXECUTABLE_NAME}.log 2>&1 &
