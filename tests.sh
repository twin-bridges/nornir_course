#!/bin/bash

# source ./env_vars

# uncomment if overriding legacy EOS gateway:
# export EOS_GATEWAY="10.0.2.2"

pylama .
black --check .
cd tests
py.test -s -v .
