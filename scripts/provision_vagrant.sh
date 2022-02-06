#!/usr/bin/env bash

set -Eeo pipefail

export DEBIAN_FRONTEND=noninteractive
apt-get update
apt-get upgrade -y
apt-get install -y apt-transport-https ca-certificates software-properties-common python3-pip

# TODO: figure out how to get around needing git for GitPython
apt-get install -y git

# install dependencies
cd /code && sudo -u vagrant pip3 install -r requirements.txt --editable .
