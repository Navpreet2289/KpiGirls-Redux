Vagrant.configure("2") do |config|
  config.vm.box = "ubuntu/trusty64"
  config.vm.synced_folder ".", "/var/webapps/girls_proj/code",
    owner: "girl_user", group: "users"
  config.vm.network :private_network, ip: "172.16.0.25"
  config.vm.network "public_network", bridge: "wlan0"
  config.vm.box_check_update = false
  config.vm.provider "virtualbox" do |v|
    v.memory = 512
    v.cpus = 1
    v.name = "GirlsRedux"
  end
end