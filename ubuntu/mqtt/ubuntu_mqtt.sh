#!/usr/bin/env bash

if [ -z ${CWD} ] || [ -z ${testmode} ] || [ -z ${verbose} ] || [ -z ${install_type} ]; then
    echo "You can not call this file directly."
    exit 1
fi

cmsg
cmsg -c "Made it to the mqtt installer file!!!"
cmsg
cmsg -g "         CWD: ${CWD}"
cmsg -g "    testmode: ${testmode}"
cmsg -g "     verbose: ${verbose}"
cmsg -g "install_type: ${install_type}"
cmsg

exit 0

apt install mosquitto mosquitto-clients


