#!/usr/bin/env bash

###
#   This script was created to remind me of all the things I like to 
#   install on Ubuntu desktop. 
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

## Output colors :-)
HL1='\e[1;94m' #HL = highlight normal  - light blue
HL2='\e[0;31m' #HL = highlight warning - light red
RST='\e[0m'    #Reset Color


## Install Snaps
#snap refresh
#snap install vlc qownnotes spotify gimp irccloud-desktop darktable inkscape


## Update, Upgrade, and autoremove
sudo apt-get update && sudo apt-get -y upgrade && sudo apt autoremove


## 3rd party codecs
sudo apt install ubuntu-restricted-extras


## Install utility applications
sudo apt-get install -y vim gnome-tweak-tool compiz compiz-gnome compiz-plugins compiz-plugins-extra compizconfig-settings-manager curl tilix htop tmux git


## Utility applications to consider installing using apt-get
#gstm - gnome ssh tunneling manager - gui for ssh tunnels (doesn't scale well on high dpi screens)


## Install Sublime Text 3
wget -qO - https://download.sublimetext.com/sublimehq-pub.gpg | sudo apt-key add -
echo "deb https://download.sublimetext.com/ apt/stable/" | sudo tee /etc/apt/sources.list.d/sublime-text.list
sudo apt-get update && sudo apt-get install -y sublime-text


## Install php 7.1 (php7.2 is already out as of 2017-11-30 you should update to include it)
sudo apt-get install -y php7.1 php7.1-cli php7.1-curl php7.1-common php7.1-json php7.1-mbstring php7.1-gd php7.1-intl php7.1-xml php7.1-mysql php7.1-mcrypt php7.1-zip


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
git config --global core.editor "vim"
#git config --global merge.tool vimdiff
git config --global diff.tool vimdiff
git config --global difftool.prompt false
git config --global alias.df diff
git config --global aliad.dt difftool


## Make Repos folder
if [ ! -d "$HOME"/repos ]; then
    cd "$HOME" && mkdir repos
fi


## Install myvimrc repo
if [ ! -f "$HOME"/repos/myvimrc/.vimrc ]; then
    echo ""
    echo -e "${HL1}Cloning the joeladam518/myvimrc github repo${RST}"
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
        echo -e "${HL1}Successfully installed the myvimrc repo${RST}"
    else
        echo -e "${HL2}Something went wrong with installing the myvimrc repo${RST}"
        exit
    fi
else
    echo -e "${HL1}.vimrc is already there${RST}"
fi

## Install mybashrc repo
if [[ ! -f "$HOME"/.bashrc.old && -f "$HOME"/.bashrc ]]; then
    echo ""
    echo -e "${HL1}Cloning the joeladam518/mybashrc github repo${RST}"
    echo ""
    
    cd "$HOME" && mv .bashrc .bashrc.old
    
    if [ -f "$HOME"/.bashrc.old ]; then
        
        if [ ! -d "$HOME"/repos ]; then
            cd "$HOME" && mkdir repos
        fi
        
        if [ ! -d "$HOME"/repos/mybashrc ]; then
            cd "$HOME"/repos && git clone "git@github.com:joeladam518/mybashrc.git"
        fi

        cd "$HOME" && ln -sf "$HOME"/repos/mybashrc/desktop/.bashrc
    else 
        echo -e "${HL2}Couldn't find .bashrc.old... Stopping what I'm doing...${RST}"
    fi
    
    if [[ -f "$HOME"/repos/mybashrc/server/.bashrc &&  -e "$HOME"/.bashrc ]]; then
        echo -e "${HL1}Successfully installed the mybashrc repo${RST}"
    else
        echo -e "${HL2}Something went wrong with install mybashrc...${RST}"
    fi
else
    echo -e "${HL1}.bashrc is already swapped out${RST}"
fi

## Install all your other repos
if [ ! -d "$HOME"/repos/multiple_button_presses ]; then
    cd "$HOME"/repos && git clone "git@github.com:joeladam518/multiple_button_presses.git"
fi
if [ ! -d "$HOME"/repos/Web_Relays ]; then
    cd "$HOME"/repos && git clone "git@github.com:joeladam518/Web_Relays.git"
fi
if [ ! -d "$HOME"/repos/ArduinoRGBLighting ]; then
    cd "$HOME"/repos && git clone "git@github.com:joeladam518/ArduinoRGBLighting.git"
fi
if [ ! -d "$HOME"/repos/rpi_scripts ]; then
    cd "$HOME"/repos && git clone "git@github.com:joeladam518/rpi_scripts.git"
fi
if [ ! -d "$HOME"/repos/rpi_api ]; then
    cd "$HOME"/repos && git clone "git@github.com:joeladam518/rpi_api.git"
fi
if [ ! -d "$HOME"/repos/update-all-servers ]; then
    cd "$HOME"/repos && git clone "git@github.com:joeladam518/update-all-servers.git"
fi
if [ ! -d "$HOME"/repos/Backup_Script ]; then
    cd "$HOME"/repos && git clone "git@github.com:joeladam518/Backup_Script.git"
fi
if [ ! -d "$HOME"/repos/htt-wp-plugin ]; then
    cd "$HOME"/repos && git clone "git@github.com:joeladam518/htt-wp-plugin.git"
fi
if [ ! -d "$HOME"/repos/ugly_sweater ]; then
    cd "$HOME"/repos && git clone "git@github.com:joeladam518/ugly_sweater.git"
fi


## Install bash-git-prompt
cd "$HOME" && git clone "https://github.com/magicmonty/bash-git-prompt.git" .bash-git-prompt --depth=1


## Install fzf
cd "$HOME" && git clone --depth 1 "https://github.com/junegunn/fzf.git" ~/.fzf
cd "$HOME" && "$HOME"/.fzf/install
set rtp+=~/.fzf


## Install your theme and icons
if [ ! -d "$HOME"/.themes ]; then
    cd "$HOME" && mkdir .themes
fi

if [ ! -d "$HOME"/.icons ]; then
    cd "$HOME" && mkdir .icons
fi


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
