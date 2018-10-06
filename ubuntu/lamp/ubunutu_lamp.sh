#!/usr/bin/env bash

# Output Colors :-)
HL1='\e[1;94m' #HL1 = highlight normal - light blue
HL2='\e[1;35m' #HL2 = highlight warning - magenta
RST='\e[0m'

echo ""
echo -e "${HL1}-- Update && Upgrade && AutoRemove --${RST}"
cd "$HOME" && apt-get update && apt-get -y upgrade && apt-get -y autoremove

echo ""
echo -e "${HL1}-- Install needed packages --${RST}"
cd "$HOME" && apt-get -y install software-properties-common
cd "$HOME" && apt-get install -y python-software-properties python3 python3-pip vim htop curl git

exit 0

#!/usr/bin/env bash

## Function
Update () {
    sudo apt-get update && sudo apt-get -y upgrade && sudo apt-get autoremove
}

## Variables

# Output Colors :-)
HL1='\e[1;94m' #HL1 = highlight normal - light blue
HL2='\e[1;35m' #HL2 = highlight warning - magenta
RST='\e[0m'

# mysql variables
db_root_pass='secret'
db_name='testenv_db'
db_user='testenv_usr'
db_pass='secret'

# Create project folder if doesn't exists
if [ ! -d "/var/www/html/public" ]; then
    mkdir "/var/www/html/public"
fi

path_to_working_dir="/var/www/html/public"

cd "$HOME" && ln -sf /var/www/html www

## Begin Configuration
echo ""
echo -e "${HL1}-- Update Upgrade --${RST}"
Update

echo ""
echo -e "${HL1}-- Force Locale --${RST}"
echo "LC_ALL=en_US.UTF-8" >> /etc/default/locale
locale-gen en_US.UTF-8

## Make Repos folder
if [ ! -d "$HOME"/repos ]; then
    cd "$HOME" && mkdir repos
fi

## Install myvimrc repo
if [ ! -f "$HOME"/repos/myvimrc/.vimrc ]; then
    echo ""
    echo -e "${HL1}-- Cloning the joeladam518/myvimrc github repo --${RST}"
    echo ""

    if [ ! -d "$HOME"/repos ]; then
        cd "$HOME" && mkdir repos
    fi

    if [ ! -d "$HOME"/repos/myvimrc ]; then
        cd "$HOME"/repos && git clone "https://github.com/joeladam518/myvimrc.git"
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
    echo -e "${HL1}-- Cloning the joeladam518/mybashrc github repo --${RST}"
    echo ""

    cd "$HOME" && mv .bashrc .bashrc.old

    if [ -f "$HOME"/.bashrc.old ]; then

        if [ ! -d "$HOME"/repos ]; then
            cd "$HOME" && mkdir repos
        fi

        if [ ! -d "$HOME"/repos/mybashrc ]; then
            cd "$HOME"/repos && git clone "https://github.com/joeladam518/mybashrc.git"
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

if ! foobar_loc="$(type -p "unzip")" || [ -z "unzip" ]; then
    echo ""
    echo -e "${HL1}-- Installing unzip -- ${RST}"
    sudo apt-get -y install zip unzip
fi

if ! foobar_loc="$(type -p "ntpdate")" || [ -z "ntpdate" ]; then
    echo ""
    echo -e "${HL1}-- Installing ntpdate --${RST}"
    sudo apt-get -y install ntpdate
fi

echo ""
echo -e "${HL1}-- Fix the UTC time -- ${RST}"
cd "$HOME"
sudo service ntp stop
sudo ntpdate -s time.nist.gov
sudo service ntp start

echo ""
echo -e "${HL1}-- Set some git config settings -- ${RST}"
cd "$HOME"
git config --global core.editor "vim"
git config --global diff.tool vimdiff
git config --global difftool.prompt false
git config --global alias.df diff
git config --global aliad.dt difftool

echo ""
echo -e "${HL1}-- Install PPA's --${RST}"
cd "$HOME"
sudo add-apt-repository ppa:ondrej/php -y
sudo add-apt-repository ppa:chris-lea/redis-server -y
Update

echo ""
echo -e "${HL1}-- Install web server packages --${RST}"
cd "$HOME"
sudo apt-get install -y apache2 redis-server
sudo apt-get install -y php7.1 php7.1-common php7.1-dev php7.1-json php7.1-opcache php7.1-cli libapache2-mod-php7.1 php7.1-mysql php7.1-fpm php7.1-curl php7.1-gd php7.1-mcrypt php7.1-mbstring php7.1-bcmath php7.1-xml php7.1-zip
Update

echo ""
echo -e "${HL1}-- Install and configure mariadb --${RST}"
cd "$HOME"
sudo apt-get install -y mariadb-server mariadb-client
#sudo mysql_secure_installation

sudo mysql -u root -p"$db_root_pass" -e "UPDATE mysql.user SET Password=PASSWORD('$db_root_pass') WHERE User='root'; FLUSH PRIVILEGES;"
sudo mysql -u root -p"$db_root_pass" -e "DELETE FROM mysql.user WHERE User='root' AND Host NOT IN ('localhost', '127.0.0.1', '::1')"
sudo mysql -u root -p"$db_root_pass" -e "DELETE FROM mysql.user WHERE User=''"
sudo mysql -u root -p"$db_root_pass" -e "DELETE FROM mysql.db WHERE Db='test' OR Db='test\_%'"
sudo mysql -u root -p"$db_root_pass" -e "GRANT ALL ON *.* TO root@'127.0.0.1' IDENTIFIED BY '$db_root_pass' WITH GRANT OPTION;"
sudo mysql -u root -p"$db_root_pass" -e "FLUSH PRIVILEGES;"

sudo mysql -u root -p"$db_root_pass" -e "CREATE DATABASE IF NOT EXISTS $db_name;"
sudo mysql -u root -p"$db_root_pass" -e "CREATE USER '$db_user'@'127.0.0.1' IDENTIFIED BY '$db_pass';"
sudo mysql -u root -p"$db_root_pass" -e "CREATE USER '$db_user'@'localhost' IDENTIFIED BY '$db_pass';"
sudo mysql -u root -p"$db_root_pass" -e "GRANT ALL ON $db_name.* TO '$db_user'@'127.0.0.1';"
sudo mysql -u root -p"$db_root_pass" -e "GRANT ALL ON $db_name.* TO '$db_user'@'localhost';"
sudo mysql -u root -p"$db_root_pass" -e "FLUSH PRIVILEGES;"

sudo service apache2 restart
sudo service mysql restart

echo ""
echo -e "${HL1}-- Configure PHP &Apache --${RST}"
cd "$HOME"
sudo sed -i "s/error_reporting = .*/error_reporting = E_ALL/" /etc/php/7.1/apache2/php.ini
sudo sed -i "s/display_errors = .*/display_errors = On/" /etc/php/7.1/apache2/php.ini

echo ""
echo -e "${HL1}-- Creating virtual hosts --${RST}"
cat << EOF | sudo tee -a /etc/apache2/sites-available/000-default.conf
<Directory "/var/www/html">
    AllowOverride All
    Require all granted
</Directory>

<VirtualHost *:80>
    DocumentRoot "/var/www/html/public"
    ServerName testenv.local
</VirtualHost>
EOF

echo ""
echo -e "${HL1}-- Enable Mod Rewrite --${RST}"
sudo a2enmod rewrite

echo ""
echo -e "${HL1}-- Restart Apache --${RST}"
sudo service apache2 restart
sudo service mysql restart

echo ""
echo -e "${HL1}-- Install Composer --${RST}"
cd "$HOME"
curl -s https://getcomposer.org/installer | php
sudo mv composer.phar /usr/local/bin/composer
sudo chmod +x /usr/local/bin/composer

echo ""
echo -e "${HL1}-- Install NodeJS --${RST}"
cd "$HOME"
sudo apt-get install -y nodejs
sudo apt-get install -y npm

echo ""
echo -e "${HL1}-- Running: composer install --${RST}"
cd "$path_to_working_dir" && composer install

echo ""
echo -e "${HL1}-- Running: npm install --${RST}"
cd "$path_to_working_dir" && npm install

cd "$path_to_working_dir" && sudo touch .htaccess

exit 0

