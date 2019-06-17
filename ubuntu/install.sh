#!/usr/bin/env bash

# Global Variables
CWD=$(pwd)

## Export provision_me's bin folder to path
export PATH="${PATH}:$(realpath "../bin")"

# Check if the user is running this script as root.
if [ $(id -u) -ne 0 ]; then
    cmsg -y "This install script needs root privileges to do it's job." 1>&2
    exit 1
fi

## Script functions
show_help() {
cat << EOF
Usage: ${0##*/} [-htv] [SERVER_NAME]...
This script helps make it easier to use the sshfs program. Uses
your ssh config file to generate the valid servers to mount.
    -h      Display this help and exit.
    -d      Install the development version of the stack
    -t      Testing mode. Will not run the sshfs command. Just echo it
    -v      Verbose mode. Can be used multiple times for increased verbosity.
EOF
}

## Parse the arguments and options for this script
development=0
testmode=0
verbose=0
OPTIND=1;
while getopts ":hdtv" opt; do
    case ${opt} in
        h)  show_help
            exit 0
            ;;
        d)  development=1
            ;;
        t)  testmode=1
            ;;
        v)  verbose=1
            ;;
        \?) cmsg -r "${0##*/} invalid option: -${OPTARG}" 1>&2
            exit 1
            ;;
    esac
done

shift $((OPTIND-1))   # Discard the options and sentinel --

## Input Variables
install_type=${1}


## Start Script

if [ $install_type = "mqtt" ]; then
    . "${CWD}/mqtt/ubuntu_mqtt.sh"
else
    cmsg -r "Invalid install type... \"${install_type}\""
    exit 1
fi

exit 0
