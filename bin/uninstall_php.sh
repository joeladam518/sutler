#!/usr/bin/env bash

## Variables
CWD=$(pwd)

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
msg_c -g "Ok, I will now try to uninstall php..."
prompt=$(msg_c -mn "Warning!!!")
prompt="${prompt} $(msg_c -mn "This command will uninstall every single php package on your system!!!")"
prompt="${prompt} $(msg_c -mn "Is that ok? [Y/n] ")"
read -t 10 -p "${prompt}" proceed_with_uninstall

if [  "$?" -ne "0" ]; then
    msg_c ""
fi

if [[ "${proceed_with_uninstall}" != "y" ]]; then
    msg_c -a "Exiting..."
    msg_c ""
    exit
fi

installed_php_packages=$(dpkg -l | grep php | sed 's/\s\{3,\}.*$//' | sed 's/^ii  //' | tr '\n' ' ')

if [ -z "${installed_php_packages}" ]; then
    msc_c -r "Couldn't find any php packages. exiting..."
    msg_c ""
    exit 1
fi

uninstall_command="sudo apt-get purge ${installed_php_packages}&& sudo apt-get --purge autoremove -y"

msg_c ""
msg_c -g "This is the command that will be executed: "
msg_c "${uninstall_command}"
msg_c ""

proceed_with_uninstall=""
prompt=$(msg_c -mn "Proceed? [Y/n] ")
read -t 10 -p "${prompt}" proceed_with_uninstall

if [  "$?" -ne "0" ]; then
    msg_c ""
fi

if [[ "${proceed_with_uninstall}" != "y" ]]; then
    msg_c -a "Exiting..."
    msg_c ""
    exit
fi

msg_c ""
msg_c -g "Starting the uninstall..."
#eval ${uninstall_command}
msg_c -g "Done!"
msg_c ""
