#!/usr/bin/env bash

## Variables
CWD=$(pwd)
default_php_version="7.2"

## Functions
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

msg_c ""
msg_c ""

msg_c -a "Ok. I am going to try and install php..."
msg_c -na "Please type in the most current version of php that you know of: "

read -t 5 php_version

msg_c ""

if [[ -z "${php_version}" ]]; then
    php_version="${default_php_version}"

    msg_c ""
    msg_c -y "You failed to specify a php version, so I will use php${php_version}"
fi

if [[ -n ${php_version//[0-9]\.[0-9]/} ]]; then
    msg_c -r "I'm sorry you should only input the php version number. example: \"7.1\""
    msg_c ""
    msg_c ""
    exit 1
fi

msg_c -ng "The php version to be installed is...  "
msg_c -ng "php${php_version}"
msg_c -g "!!!"

#php${php_version}-mcrypt // dosent exist anymore

msg_c ""
msg_c -c "Creating the install command"
install_command="sudo apt-get install -y"
install_command="${install_command} php${php_version} php${php_version}-cli php${php_version}-curl"
install_command="${install_command} php${php_version}-common php${php_version}-json"
install_command="${install_command} php${php_version}-mbstring php${php_version}-gd php${php_version}-intl"
install_command="${install_command} php${php_version}-xml php${php_version}-mysql"
install_command="${install_command} php${php_version}-zip php${php_version}-pgsql"
msg_c -c "Done!"

msg_c ""
msg_c -c "Echoing the install command: "
#msg_c -y "${install_command}"
eval ${install_command}

msg_c ""
msg_c ""
