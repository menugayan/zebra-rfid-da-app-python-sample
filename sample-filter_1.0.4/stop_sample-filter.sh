EXECUTABLE_NAME=sample-filter
PID=`ps -C 'python3 /apps/${EXECUTABLE_NAME}.py' -o pid=`
kill -9 $PID
unset EXECUTABLE_NAME
unset PID
