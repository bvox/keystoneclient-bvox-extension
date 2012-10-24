#!/usr/bin/env bash
TOOLS=`dirname $0`
VENV=$TOOLS/../.venv
source $VENV/bin/activate && "$@"
