#!/usr/bin/env bash

if ! ([ -n "$CWD" ] && [ -n "$platform" ] && [ "$provision_type" = "lemp" ]); then 
    echo "You can not call this file directly." 1>&2
    exit 1
fi

cmsg -c "Made it to the lemp.sh script."
