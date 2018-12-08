#!/usr/bin/env bash

## Variables
CWD=$(pwd)
install_php=$(realpath "${CWD}/../../bin/install_php.sh")

# mysql variables
db_root_pass='secret'
db_name='testenv_db'
db_user='testenv_usr'
db_pass='secret'

## Global functions
source "${CWD}/../../global/functions.sh"

## Script Specific Functions
AUU() {
    msg_c -c "-- Update && Upgrade && AutoRemove --"
    #-------------------------------------------------
    cd ${HOME} && sudo apt-get update && sudo apt-get -y upgrade && sudo apt-get -y autoremove
    #-------------------------------------------------
    msg_c -c "done!"
}

echo ""
msg_c -c "-- Install needed packages --"
#-----------------------------------------------------------------------------------------------
cd "$HOME" && apt-get -y install software-properties-common
cd "$HOME" && apt-get install -y python-software-properties python3 python3-pip vim htop curl git
#------------------------------------------------------------------------------------------------
msg_c -c "done!"
exit 0


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


## Install myvimrc repo


## Install mybashrc repo


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

