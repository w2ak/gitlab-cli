#!/bin/sh
export PYTHONPATH="${PYTHONPATH:-}:$(dirname "$(readlink -e "$0")")"
python3 -m gitlab $@
