#!/usr/bin/env bash

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

install_mybashrc() {
    if [ -z "${1}" ] || ([ ${1} != "desktop" ] && [ ${1} != "mac" ] && [ ${1} != "server" ]); then
        msg_c -nr "Must specify a type of system. "
        msg_c -a  "Valid types: {desktop|mac|server}"
        return
    fi

    if [[ ! -d "${HOME}/repos/mybashrc" && ! -f "${HOME}/.bashrc.old" ]]; then
        echo ""
        msg_c -c "-- Cloning the joeladam518/mybashrc github repo --"
        echo ""

        if [ ! -d "$HOME"/repos ]; then
            cd "$HOME" && mkdir repos
        fi

        cd "${HOME}" && mv .bashrc .bashrc.old

        if [ -f "${HOME}/.bashrc.old" ]; then
            msg_c -r "Couldn't find the .bashrc.old file, so I'm going to stop what I'm doing right here."
            return
        fi

        if [ ! -d "${HOME}/repos/mybashrc" ]; then
            cd "${HOME}/repos" && git clone "https://github.com/joeladam518/mybashrc.git"
        fi

        cd "${HOME}" && ln -sf "${HOME}/repos/mybashrc/${1}/.bashrc"

        if [[ -f "${HOME}/repos/mybashrc/${1}/.bashrc" &&  -e "${HOME}/.bashrc" ]]; then
            msg_c -g "Successfully installed the mybashrc repo."
        else
            msg_c -r "Something went wrong with installing mybashrc."
        fi
    else
        msg_c -y "This system's .bashrc is already swapped out with mybashrc."
    fi
}

install_myvimrc() {
    if [ ! -f "${HOME}/repos/myvimrc/.vimrc" ]; then
        echo ""
        msg_c -c "-- Cloning the joeladam518/myvimrc github repo --"
        echo ""

        if [ ! -d "${HOME}/repos"]; then
            cd "$HOME" && mkdir repos
        fi

        if [ ! -d "${HOME}/repos/myvimrc" ]; then
            cd "${HOME}/repos" && git clone "https://github.com/joeladam518/myvimrc.git"
        fi

        cd "${HOME}" && ln -sf "$HOME"/repos/myvimrc/.vim
        cd "${HOME}" && ln -sf "$HOME"/repos/myvimrc/.vimrc

        if [[ -f "${HOME}/repos/myvimrc/.vimrc" &&  -e "${HOME}/.vimrc" ]]; then
            msc_c -g "Successfully installed the myvimrc repo."
        else
            msg_c -r "Something went wrong with installing the myvimrc repo."
        fi
    else
        msg_c -y ".vimrc is already there."
    fi
}