#!/usr/bin/env bash

SCRIPTS_DIR="$(cd "$(dirname "$0")" > /dev/null 2>&1 && pwd -P)"
PROJECT_DIR="$(dirname "$SCRIPTS_DIR")"

cd "${PROJECT_DIR}" && exit 1

if [ -n "${SETUP_VIRTUALENV:-""}" ]; then
    if command -v "virtualenv" >/dev/null 2>&1; then
        virtualenv venv
    elif python3 -c "import venv" >/dev/null 2>&1; then
        python3 -m venv venv
    else
        echo "Can not create a virtual environment." 2>&1
        exit 1
    fi

    source venv/bin/activate
fi

pip install -r requirements.txt pyinstaller
pyinstaller \
    --noconfirm \
    --log-level=WARN \
    --clean \
    --onefile \
    --nowindow \
    --name=sutler \
    "${PROJECT_DIR}/sutler.spec"

if [ -n "${SETUP_VIRTUALENV:-""}" ]; then
    deactivate
fi
