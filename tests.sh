#!/bin/bash

# source ./env_vars

# uncomment if overriding legacy EOS gateway:
# export EOS_GATEWAY="10.0.2.2"

RETURN_CODE=0

echo "pylama ." \
&& pylama . \
&& echo "black" \
&& black --check . \
&& echo "running pytest..." \
&& cd tests \
&& py.test -x -s -v test_class* \
&& py.test -x -s -v test_bonus* \
\
|| RETURN_CODE=1

exit $RETURN_CODE
