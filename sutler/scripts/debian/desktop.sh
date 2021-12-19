#!/usr/scripts/env bash

if ! ([ -n "$CWD" ] && [ -n "$platform" ] && [ "$provision_type" = "desktop" ]); then
    echo "You can not call this file directly." 1>&2
    exit 1
fi

#----------------------------------------------------------------------------------------------------

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

#----------------------------------------------------------------------------------------------------
# Start Script

msg_c -c "apt-get update and upgrade"
#----------------------------------------------------------------------------------------------------
apt-update-upgrade
#----------------------------------------------------------------------------------------------------
msg_c -c "Done!"

msg_c -c "Installing Fun stuff"
#----------------------------------------------------------------------------------------------------
sudo apt install -y software-properties-common build-essential
#----------------------------------------------------------------------------------------------------
msg_c -c "Done!"

msg_c -c "Installing restricted extras"
#----------------------------------------------------------------------------------------------------
sudo apt install ubuntu-restricted-extras ubuntu-restricted-addons
#----------------------------------------------------------------------------------------------------
msg_c -c "Done!"

msg_c -c "Installing utility applications"
#----------------------------------------------------------------------------------------------------
sudo apt install -y gnome-tweak-tool git vim-gtk3 tmux curl tilix htop tree mysql-client mosquitto-clients sshfs xsel
#----------------------------------------------------------------------------------------------------
msg_c -c "Done!"

msg_c -c "Installing the ability to work with exfat drives"
#----------------------------------------------------------------------------------------------------
sudo apt install -y exfat-utils exfat-fuse
#----------------------------------------------------------------------------------------------------
msg_c -c "Done!"

msg_c -c "Installing dconf editor for changing settings in gnome"
#----------------------------------------------------------------------------------------------------
#sudo apt-get install -y dconf-editor
#----------------------------------------------------------------------------------------------------
msg_c -c "Done!"

msg_c -c "Installing snaps"
#----------------------------------------------------------------------------------------------------
snap refresh
snap install vlc qownnotes spotify gimp irccloud-desktop darktable inkscape
#----------------------------------------------------------------------------------------------------
msg_c -c "Done!"

msg_c -c "Installing SublimeText 3"
#----------------------------------------------------------------------------------------------------
wget -qO - https://download.sublimetext.com/sublimehq-pub.gpg | sudo apt-key add -
echo "deb https://download.sublimetext.com/apt/stable/" | sudo tee /etc/apt/sources.list.d/sublime-text.list
sudo apt-get update && sudo apt-get install -y sublime-text
#----------------------------------------------------------------------------------------------------
msg_c -c "Done!"

# Install php!
msg_c -c "Installing php"
#----------------------------------------------------------------------------------------------------
php-installer "7.4"
#----------------------------------------------------------------------------------------------------
msg_c -c "Done!"

## Install Composer
msg_c -c "Installing Composer"
#----------------------------------------------------------------------------------------------------
cd "$HOME" && php-installer-composer
#----------------------------------------------------------------------------------------------------
msg_c -c "Done!"

# Install node.js and npm
msg_c -c "Installing nodejs and npm"
#----------------------------------------------------------------------------------------------------
cd "$HOME" && install-nodejs "14" "$platform"
#----------------------------------------------------------------------------------------------------
msg_c -c "Done!"

msg_c -c "Installing python3-pip"
#----------------------------------------------------------------------------------------------------
sudo apt-get install -y python3-pip
#----------------------------------------------------------------------------------------------------
msg_c -c "Done!"

# Set the default editor
sudo update-alternatives --config editor

# Create ssh keys
msg_c -c "Create ssh keys"
#----------------------------------------------------------------------------------------------------
if [ ! -f "$HOME"/.ssh/id_rsa ]; then
    if [ ! -d "$HOME"/.ssh ]; then
        cd "$HOME" && mkdir .ssh
    fi

    cd "$HOME"/.ssh && ssh-keygen -t rsa
fi
#----------------------------------------------------------------------------------------------------
msg_c -c "Done!"

msg_c -c "Install dotfiles"
#----------------------------------------------------------------------------------------------------
cd "$HOME" && install-dotfiles
#----------------------------------------------------------------------------------------------------
msg_c -c "Done!"

msg_c -c "Install bash-git-prompt"
#----------------------------------------------------------------------------------------------------
cd "$HOME" && git clone "https://github.com/magicmonty/bash-git-prompt.git" .bash-git-prompt --depth=1
#----------------------------------------------------------------------------------------------------
msg_c -c "Done!"

msg_c -c "Install fzf"
#----------------------------------------------------------------------------------------------------
cd "$HOME" && install-fzf
#----------------------------------------------------------------------------------------------------
msg_c -c "Done!"


msg_c -c "Install make the Ubuntu themes and icons folders"
#----------------------------------------------------------------------------------------------------
if [ ! -d "$HOME"/.themes ]; then
    cd "$HOME" && mkdir .themes
fi

if [ ! -d "$HOME"/.icons ]; then
    cd "$HOME" && mkdir .icons
fi
#----------------------------------------------------------------------------------------------------
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
