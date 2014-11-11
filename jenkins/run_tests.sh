#!/usr/bin/env bash

set -e
export PATH=/opt/python/bin:$PATH
echo "############################ Run tests ############################"
./run_integration_tests.sh
