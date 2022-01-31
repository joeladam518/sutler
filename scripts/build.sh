#!/usr/bin/env bash

SCRIPTS_DIR="$(cd "$(dirname "$0")" > /dev/null 2>&1 && pwd -P)"
PROJECT_DIR="$(dirname "$SCRIPTS_DIR")"

pyinstaller \
  --noconfirm \
  --log-level=WARN \
  --clean \
  --onefile \
  --nowindow \
  --name=sutler \
  "${PROJECT_DIR}/sutler.spec"
