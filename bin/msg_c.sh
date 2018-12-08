#!/usr/bin/env bash

# Output messages in color! :-)

OPTIND=1
newline="1"
CHOSEN_COLOR=""
RESET=$(tput sgr0)

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
