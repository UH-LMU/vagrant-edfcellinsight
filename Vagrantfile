# -*- mode: ruby -*-
# vi: set ft=ruby :

# All Vagrant configuration is done below. The "2" in Vagrant.configure
# configures the configuration version (we support older styles for
# backwards compatibility). Please don't change it unless you know what
# you're doing.
Vagrant.configure(2) do |config|
  config.vm.box = "ubuntu/xenial64"

  # config.vm.synced_folder "../data", "/vagrant_data"

  config.vm.provider "virtualbox" do |vb|
    # Customize the amount of memory on the VM:
    vb.memory = "8196"
    #vb.memory = "16392"
  end

  config.vm.provision "ansible_local" do |ansible|
    ansible.playbook = "provision.yml"
  end

#  config.vm.provision "shell", inline: <<-SHELL
#    sudo apt-get update
#    sudo apt-get install -y imgcnv
#  SHELL
end
