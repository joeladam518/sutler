#!/usr/scripts/env bash

if ! { [ -n "$CWD" ] && [ -n "$platform" ] && [ "$provision_type" = "mqtt" ]; }; then
    echo "You can not call this file directly." 1>&2
    exit 1
fi

# Variables
mqtt_auth_user="jhaker"
mqtt_default_config_path="/etc/mosquitto/conf.d/default.conf"
server_domain="mqtt.joelhaker.com"

# Start provisioning
cmsg
cmsg -c "installing mosiquitto mqtt server"
apt-get install -y mosquitto mosquitto-clients
cmsg -c "done!"

cmsg
cmsg

cmsg -y "This next part requires your attention!"

cmsg
cmsg

prompt=$(cmsg -mn "Are you ready? [y/N] ")
read -r -t 10 -p "$prompt" response

if [  "$?" -ne "0" ]; then
    cmsg
fi

if [[ ! "$response" =~ ^([yY][eE][sS]|[yY])+$ ]]; then
    cmsg -r "I'm so sorry that you have the attention span of a goldfish...." 1>&2
    exit 1
fi

cmsg
cmsg -c "Great! Please enter the password you would like to use for you the user [${mqtt_auth_user}]: "
mosquitto_passwd -c /etc/mosquitto/passwd ${mqtt_auth_user}

cmsg
cmsg

cmsg -y "Ok, I'm done needing your attention"

cmsg
cmsg

cmsg -c "Writing the default config to: ${mqtt_default_config_path}"
#----------------------------------------------
if [ "${development}" -eq "1" ]; then

cat > ${mqtt_default_config_path} << EOF
    allow_anonymous true
    password_file /etc/mosquitto/passwd

    listener 1883
    protocol mqtt

    listener 9001
    protocol websockets

EOF

else

cat > ${mqtt_default_config_path} << EOF
    allow_anonymous false
    password_file /etc/mosquitto/passwd

    listener 1883 localhost

    listener 8883
    certfile /etc/letsencrypt/live/${server_domain}/cert.pem
    cafile /etc/letsencrypt/live/${server_domain}/chain.pem
    keyfile /etc/letsencrypt/live/${server_domain}/privkey.pem

    listener 8083
    protocol websockets
    certfile /etc/letsencrypt/live/${server_domain}/cert.pem
    cafile /etc/letsencrypt/live/${server_domain}/chain.pem
    keyfile /etc/letsencrypt/live/${server_domain}/privkey.pem

EOF

fi
#----------------------------------------------
cmsg -c "done!..."

cmsg
cmsg

cmsg -c "Set the fire wall"
#----------------------------------------------
if [ "${development}" -eq "1" ]; then
    ufw allow 1883
    ufw allow 9001
else
    ufw allow 8883
    ufw allow 8083
fi
#----------------------------------------------
cmsg -c "done!..."

cmsg
cmsg

cmsg -c "Restarting the mosquitto server"
#----------------------------------------------
systemctl restart mosquitto
#----------------------------------------------
cmsg -c "done!..."

cmsg
cmsg

cmsg -g "Done installing the mqtt server"
