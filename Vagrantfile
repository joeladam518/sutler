# -*- mode: ruby -*-
# vi: set ft=ruby :

Vagrant.configure("2") do |config|
    # For a complete list of configuration options, please see the
    # documentation at https://docs.vagrantup.com.
    config.vm.synced_folder ".", "/code"

    config.vm.define "ubuntu", primary: true do |ubuntu|
        ubuntu.vm.box = "bento/ubuntu-20.04"
        ubuntu.vm.hostname = 'sutlerbox-ubuntu'
        ubuntu.vm.network "private_network", ip: "192.168.200.200"

        # Provider-specific configuration
        ubuntu.vm.provider "virtualbox" do |vb|
            vb.gui = false
            vb.name = 'sutlerbox-ubuntu'
            vb.memory = 4096
            vb.cpus = 1
        end

        # Provision the machine
        ubuntu.vm.provision "shell", path: "scripts/provision_vagrant.sh"
    end

    config.vm.define "debian", autostart: false do |debian|
        debian.vm.box = "bento/debian-11"
        debian.vm.hostname = 'sutlerbox-debian'
        debian.vm.network "private_network", ip: "192.168.200.201"

        # Provider-specific configuration
        debian.vm.provider "virtualbox" do |vb|
            vb.gui = false
            vb.name = 'sutlerbox-debian'
            vb.memory = 4096
            vb.cpus = 1
        end

        # Provision the machine
        debian.vm.provision "shell", path: "scripts/provision_vagrant.sh"
    end
end
