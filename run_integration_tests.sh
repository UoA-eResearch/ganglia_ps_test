#!/bin/bash

export PYTHONPATH=$PYTHONPATH:./lib:./tests
python tests/gmond_collector.py
