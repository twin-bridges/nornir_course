#!/bin/bash

# source ./env_vars

pylama .
black --check .
cd tests
py.test -s -v .
