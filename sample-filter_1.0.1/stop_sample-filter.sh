#!/bin/bash
EXECUTABLE_NAME=sample_filter
PID=$(ps -C "python3 /apps/${EXECUTABLE_NAME}.py" -o pid= | tr -d ' ')
if [ -n "$PID" ]; then
    kill -9 $PID
fi
unset EXECUTABLE_NAME
unset PID
