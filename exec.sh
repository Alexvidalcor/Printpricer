#!/usr/bin/env bash

set -e
parent_path=$( cd "$(dirname "${BASH_SOURCE[0]}")" ; pwd -P )
cd "$parent_path"

source MainEnv/bin/activate
python3 main.py
deactivate
