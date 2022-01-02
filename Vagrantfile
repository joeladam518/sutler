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

    config.vm.synced_folder ".", "/code"

    config.vm.define "ubuntu", primary: true do |ubuntu|
        ubuntu.vm.box = "bento/ubuntu-20.04"
        ubuntu.vm.hostname = 'sutlerbox-ubuntu'
        ubuntu.vm.network "private_network", ip: "192.168.200.200"

        # Provider-specific configuration so you can fine-tune various
        # backing providers for Vagrant. These expose provider-specific options.
        # Example for VirtualBox:
        ubuntu.vm.provider "virtualbox" do |vb|
            vb.gui = false
            vb.name = 'sutlerbox-ubuntu'
            vb.memory = 4096
            vb.cpus = 1
        end

        # Provision the machine
        ubuntu.vm.provision "shell", path: "scripts/provision.sh"
    end

    config.vm.define "debian", autostart: false do |debian|
        debian.vm.box = "bento/debian-11"
        debian.vm.hostname = 'sutlerbox-debian'
        debian.vm.network "private_network", ip: "192.168.200.201"

        # Provider-specific configuration so you can fine-tune various
        # backing providers for Vagrant. These expose provider-specific options.
        # Example for VirtualBox:
        debian.vm.provider "virtualbox" do |vb|
            vb.gui = false
            vb.name = 'sutlerbox-debian'
            vb.memory = 4096
            vb.cpus = 1
        end

        # Provision the machine
        debian.vm.provision "shell", path: "scripts/provision.sh"
    end
end
