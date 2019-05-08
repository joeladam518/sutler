#!/usr/bin/env bash

## Variables
CWD=$(pwd)
default_php_version="7.3"

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
msg_c -g "Ok, I am going to try and install php..."

prompt=$(msg_c -mn "Please type in the most current version of php that you know of: ")
read -t 7 -p "${prompt}" php_version

if [  "$?" -ne "0" ]; then
    msg_c ""
fi

if [[ -z "${php_version}" ]]; then
    php_version="${default_php_version}"

    msg_c ""
    prompt=$(msg_c -mn "You failed to specify a php version, so I will use")
    prompt="${prompt} $(msg_c -yn "php${php_version}")"
    prompt="${prompt} $(msg_c -mn "is that ok? [Y/n] ")"
    read -t 10 -p "${prompt}" proceed_with_install

    if [  "$?" -ne "0" ]; then
        msg_c ""
    fi

    if [[ "${proceed_with_install}" != "y" ]]; then
        msg_c -a "Exiting..."
        msg_c ""
        exit
    fi
fi

if [[ -n ${php_version//[0-9]\.[0-9]/} ]]; then
    msg_c -r "I'm sorry you should only input the php version number. example: \"7.1\""
    msg_c ""
    exit 1
fi

##
## Notes:
## php${php_version}-mcrypt doesn't exist anymore
##

install_command="sudo apt-get install -y"
install_command="${install_command} php${php_version} php${php_version}-common php${php_version}-cli"
install_command="${install_command} php${php_version}-fpm php${php_version}-curl php${php_version}-json"
install_command="${install_command} php${php_version}-mbstring php${php_version}-gd php${php_version}-intl"
install_command="${install_command} php${php_version}-pgsql php${php_version}-mysql"
install_command="${install_command} php${php_version}-xml php${php_version}-zip "

msg_c ""
msg_c -g "This is the command that will be executed: "
msg_c "${install_command}"

msg_c ""
proceed_with_install=""
prompt=$(msg_c -mn "Proceed? [Y/n] ")
read -t 10 -p "${prompt}" proceed_with_install

if [  "$?" -ne "0" ]; then
    msg_c ""
fi

if [[ "${proceed_with_install}" != "y" ]]; then
    msg_c -a "Exiting..."
    msg_c ""
    exit
fi

msg_c ""
msg_c -g "Starting the install:"
#eval ${install_command}
msg_c -g "Done!"
msg_c ""
