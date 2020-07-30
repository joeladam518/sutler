#!/usr/bin/env bash

if ! ([ -n "$CWD" ] && [ "$platform" == "ubuntu" ] && [ "$provision_type" == "desktop" ]); then 
    echo "You can not call this file directly." 1>&2
    exit 1
fi

cmsg -c "Made it to the desktop.sh script."
exit

###
#   This script was created to remind me of all the things I like to
#   install on my Ubuntu desktop.
#
#   Themes that I like:
#   https://github.com/nana-4/materia-theme
#   https://github.com/adapta-project/adapta-gtk-theme
#
#   Icons that I like
#   https://github.com/PapirusDevelopmentTeam/papirus-icon-theme
#   https://github.com/cbrnix/Newaita
#
#
#   It MUST be reviewed each time and updated.
#
#   Notes:
#
#   Color for terminal screen (to mimic iTerm):
#   -------------------------------------------
#   black dark   = #000000   black light    = #686868
#   red dark     = #c91b00   red light      = #ff6e67
#   green dark   = #00c200   green light    = #5ffa68
#   yellow dark  = #C7B700   yellow light   = #fffc67
#   blue dark    = #0532e1   blue light     = #5075ff #42A5F5
#   magenta dark = #ca30c7   magenta light  = #ff77ff
#   cyan dark    = #00c5c7   cyan light     = #60fdff
#   white dark   = #D7D7D7   white light    = #ffffff
###


exit 0

##------------------------------------------------------------------------------------------------##

## Start Script

msg_c -c "Update, Upgrade, and Autoremove"
sudo apt-get update && sudo apt-get -y upgrade && sudo apt autoremove
msg_c -c "Done!"

msg_c -c "Install restricted extras"
sudo apt install ubuntu-restricted-extras ubuntu-restricted-addons
msg_c -c "Done!"

msg_c -c "Install utility applications"
sudo apt-get install -y git vim-gnome tmux curl tilix htop tree mysql-client
msg_c -c "Done!"

msg_c -c "Install the sshfs"
sudo apt-get install -y sshfs
msg_c -c "Done!"

msg_c -c "Install gnome tweak tool and compiz"
sudo apt-get install -y gnome-tweak-tool
sudo apt-get install -y compiz compiz-gnome compiz-plugins compiz-plugins-extra compizconfig-settings-manager
msg_c -c "Done!"

msg_c -c "Install the ability to work with exfat drives"
sudo apt-get install -y exfat-fuse exfat-utils
msg_c -c "Done!"

msg_c -c "install dconf editor for changing settings in gnome"
sudo apt-get install -y dconf-editor

## Install Sublime Text 3
msg_c -c "Install SublimeText 3"
wget -qO - https://download.sublimetext.com/sublimehq-pub.gpg | sudo apt-key add -
echo "deb https://download.sublimetext.com/apt/stable/" | sudo tee /etc/apt/sources.list.d/sublime-text.list
sudo apt-get update && sudo apt-get install -y sublime-text
msg_c -c "Done!"

## Install php 7.1 (php7.2 is already out as of 2017-11-30 you should update to include it)
msg_c -c "Install PHP"
sudo apt-get install -y php7.1 \
php7.1-cli \
php7.1-curl \
php7.1-common \
php7.1-json \
php7.1-mbstring \
php7.1-gd \
php7.1-intl \
php7.1-xml \
php7.1-mysql \
php7.1-mcrypt \
php7.1-zip
msg_c -c "Done!"

msg_c -c "Installing snaps"
snap refresh
snap install vlc qownnotes spotify gimp irccloud-desktop darktable inkscape
msg_c -c "Done!"

## Install Composer
cd "$HOME"
php -r "copy('https://getcomposer.org/installer', 'composer-setup.php');"
php composer-setup.php
php -r "unlink('composer-setup.php');"
sudo mv composer.phar /usr/local/bin/composer


## Install Python3 pip
sudo apt-get install -y  python3-pip


## Install node.js and npm
curl -sL https://deb.nodesource.com/setup_8.x | sudo -E bash -
sudo apt-get install -y nodejs


## Set vim as the default editor
sudo update-alternatives --config editor


## Create ssh keys
if [ ! -f "$HOME"/.ssh/id_rsa ]; then
    if [ ! -d "$HOME"/.ssh ]; then
        cd "$HOME" && mkdir .ssh
    fi

    cd "$HOME"/.ssh && ssh-keygen -t rsa
fi


## Set some Git config settings
cd "$HOME"
git config --global user.name "Joel Haker"
git config --global user.email "joeladam@gmail.com"
git config --global core.editor "vim"
git config --global diff.tool vimdiff
git config --global difftool.prompt false
#git config --global alias.df diff
#git config --global aliad.dt difftool
#git config --global merge.tool vimdiff


## Make Repos folder
if [ ! -d "$HOME"/repos ]; then
    cd "$HOME" && mkdir repos
fi


## Install myvimrc repo
if [ ! -f "$HOME"/repos/myvimrc/.vimrc ]; then
    echo ""
    msg_c -g "Cloning the joeladam518/myvimrc github repo"
    echo ""

    if [ ! -d "$HOME"/repos ]; then
        cd "$HOME" && mkdir repos
    fi

    if [ ! -d "$HOME"/repos/myvimrc ]; then
        cd "$HOME"/repos && git clone "git@github.com:joeladam518/myvimrc.git"
    fi

    cd "$HOME" && ln -sf "$HOME"/repos/myvimrc/.vim
    cd "$HOME" && ln -sf "$HOME"/repos/myvimrc/.vimrc

    if [[ -f "$HOME"/repos/myvimrc/.vimrc &&  -e "$HOME"/.vimrc ]]; then
        msg_c -g "Successfully installed the myvimrc repo"
    else
        msg_c -r "Something went wrong with installing the myvimrc repo"
    fi
else
    msg_c -y ".vimrc is already installed"
fi

## Install mybashrc repo
if [[ ! -f "$HOME"/.bashrc.old && -f "$HOME"/.bashrc ]]; then
    echo ""
    msg_c -g "Cloning the joeladam518/mybashrc github repo"

    cd "$HOME" && mv .bashrc .bashrc.old

    if [ -f "$HOME"/.bashrc.old ]; then
        if [ ! -d "$HOME"/repos ]; then
            cd "$HOME" && mkdir repos
        fi

        if [ ! -d "$HOME"/repos/mybashrc ]; then
            cd "$HOME"/repos && git clone "git@github.com:joeladam518/mybashrc.git"
        fi

        cd "$HOME" && ln -sf "$HOME"/repos/mybashrc/desktop/.bashrc

        if [[ -f "$HOME"/repos/mybashrc/server/.bashrc && -e "$HOME"/.bashrc ]]; then
            msg_c -g "Successfully installed the mybashrc repo"
        else
            msg_c -r "Something went wrong with install mybashrc..."
        fi
    else
        msg_c -r "Couldn't find .bashrc.old... Stopping what I'm doing..."
    fi
else
    msg_c -y ".bashrc is already swapped out"
fi

## Install all your other repos
echo ""
msg_c -m "Now you can go ahead and install your other repos"
echo ""

## Install bash-git-prompt
msg_c -c "Install bash-git-prompt"
cd "$HOME" && git clone "https://github.com/magicmonty/bash-git-prompt.git" .bash-git-prompt --depth=1
msg_c -c "Done!"


## Install fzf
msg_c -c "Install fzf"
cd "$HOME" && git clone --depth 1 "https://github.com/junegunn/fzf.git" ~/.fzf
cd "$HOME" && "$HOME"/.fzf/install
set rtp+=~/.fzf
msg_c -c "Done!"


## Install your theme and icons
msg_c -c "Install make the Ubuntu themes and icons folders"
if [ ! -d "$HOME"/.themes ]; then
    cd "$HOME" && mkdir .themes
fi

if [ ! -d "$HOME"/.icons ]; then
    cd "$HOME" && mkdir .icons
fi
msg_c -c "Done!"


## Install things that you can can't install via package manager
# android studio
# arduino
# chrome
# dbeaver
# git kracken
# postman
# opera
# sql electron
# Virtual-Box
# Vagrant
# Dropbox
# Slack
# gitg
# git cola
# ripit
#
