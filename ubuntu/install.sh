#!/usr/bin/env bash

## Check if the user is running this script as root. 
# if [ $(id -u) -ne 0 ]; then 
#     echo "This install script needs root privileges to do it's job." 1>&2
#     exit 1
# fi

## Script functions
determine_computer_type() {
    local machine
    local unameOut="$(uname -s)"

    case "${unameOut}" in
        Linux*)     machine="Linux"   ;;
        Darwin*)    machine="Mac"     ;;
        CYGWIN*)    machine="Cygwin"  ;;
        *)          machine="UNKNOWN" ;;
    esac

    echo ${machine}
}
msg_c() { # Output messages in color! :-)
    local OPTIND=1; local o; local newline="1"; local CHOSEN_COLOR; local RESET=$(tput sgr0);
    while getopts ":ndrgbcmya" o; do
        case "${o}" in 
            n) newline="0" ;; # no new line
            d) CHOSEN_COLOR=$(tput bold) ;;    # bold
            r) CHOSEN_COLOR=$(tput setaf 1) ;; # color red
            g) CHOSEN_COLOR=$(tput setaf 2) ;; # color green
            b) CHOSEN_COLOR=$(tput setaf 4) ;; # color blue
            c) CHOSEN_COLOR=$(tput setaf 6) ;; # color cyan
            m) CHOSEN_COLOR=$(tput setaf 5) ;; # color magenta
            y) CHOSEN_COLOR=$(tput setaf 3) ;; # color yellow
            a) CHOSEN_COLOR=$(tput setaf 7) ;; # color gray
            \? ) echo "msg_c() invalid option: -${OPTARG}"; return ;;
        esac
    done
    shift $((OPTIND - 1))
    if [ ! -z $CHOSEN_COLOR ] && [ $newline == "1" ]; then
        echo -e "${CHOSEN_COLOR}${1}${RESET}"
    elif [ ! -z $CHOSEN_COLOR ] && [ $newline == "0" ]; then  
        echo -ne "${CHOSEN_COLOR}${1}${RESET}"
    elif [ -z $CHOSEN_COLOR ] && [ $newline == "0" ]; then  
        echo -n "${1}"
    else
        echo "${1}"
    fi
}
show_help() {
cat << EOF
Usage: ${0##*/} [-htv] [SERVER_NAME]...
This script helps make it easier to use the sshfs program. Uses
your ssh config file to generate the valid servers to mount.
    -h      Display this help and exit.
    -t      Testing mode. Will not run the sshfs command. Just echo it   
    -v      Verbose mode. Can be used multiple times for increased verbosity.
EOF
}


## Global Variables
CWD=$(pwd)
t_arg=0
r_arg=""


## Parse the arguments and options for this script 
OPTIND=1;
while getopts ":htr:" opt; do
    case ${opt} in
        h)  show_help
            exit 0
            ;;
        t)  t_arg=1
            ;;
        r)  r_arg="${OPTARG}"
            ;;
        \?) msg_c -r "${0##*/} invalid option: -${OPTARG}" 1>&2
            exit 1
            ;;
    esac
done
shift "$((OPTIND - 1))"   # Discard the options and sentinel --


## Start Script


echo "CWD: ${CWD}"

echo "t_arg: ${t_arg}"

echo "r_arg: ${r_arg}"

echo "\$1: ${1}"

echo "\$2: ${2}"