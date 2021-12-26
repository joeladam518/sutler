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
    #config.vm.box = "bento/debian-11"
    config.vm.hostname = 'sutlerbox'
    config.vm.network "private_network", ip: "192.168.200.200"
    config.vm.synced_folder ".", "/code"

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
        apt-get upgrade -y
        apt-get install -y apt-transport-https ca-certificates software-properties-common python3-pip

        # TODO: figure out how to get around needing git for GitPython
        apt-get install git

        # Create the home bin directory
        mkdir -p /home/vagrant/bin
        chown vagrant:vagrant /home/vagrant/bin
        chmod 0755 /home/vagrant/bin

        # Link to the proxy script so you develop
        cd /home/vagrant/bin && ln -s /code/scripts/sutler
        cd /code && pip3 install -r requirements.txt --editable .
    SHELL
end
