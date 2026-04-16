#!/bin/bash
EXECUTABLE_NAME=hello_world
PID=$(ps aux | grep "python3 /apps/${EXECUTABLE_NAME}.py" | grep -v grep | awk '{print $2}')
if [ -n "$PID" ]; then
    kill -9 $PID
    echo "Stopped hello-world app (PID: $PID)"
else
    echo "hello-world app not running"
fi
unset EXECUTABLE_NAME
unset PID
