# -*- mode: ruby -*-
# vi: set ft=ruby :

# All Vagrant configuration is done below. The "2" in Vagrant.configure
# configures the configuration version (we support older styles for
# backwards compatibility). Please don't change it unless you know what
# you're doing.
Vagrant.configure("2") do |config|
    # The most common configuration options are documented and commented below.
    # For a complete reference, please see the online documentation at
    # https://docs.vagrantup.com.

    config.vm.box = "bento/ubuntu-20.04"
    config.vm.hostname = 'sutlerbox'
    config.vm.network "private_network", ip: "192.168.200.200"
    config.vm.synced_folder ".", "/home/vagrant/repos/sutler"

    # Provider-specific configuration so you can fine-tune various
    # backing providers for Vagrant. These expose provider-specific options.
    # Example for VirtualBox:
    config.vm.provider "virtualbox" do |vb|
        vb.gui = false
        vb.name = 'sutlerbox'
        vb.memory = 4096
        vb.cpus = 2
    end

    # Provision the machine
    config.vm.provision "shell", inline: <<-SHELL
        apt-get update
        apt-get upgrade
        apt-get install -y apt-transport-https ca-certificates software-properties-common python3-pip
        mkdir -p /home/vagrant/bin
        cat > /home/vagrant/bin/sutler << EOF
#!/usr/bin/env bash
python3 /home/vagrant/repos/sutler/sutler "\$@"
EOF
        chown vagrant:vagrant /home/vagrant/bin/sutler
        chmod 0755 /home/vagrant/bin/sutler
        pip3 install --editable /home/vagrant/repos/sutler
    SHELL
end