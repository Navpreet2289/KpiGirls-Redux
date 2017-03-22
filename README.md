Installation
============

Starting development
--------------------

Initial requirements:  

* `VirtualBox`  
* `Vagrant`  
* `Ansible`   

Steps to start development from command line:
1. Set absolute paths in `deployment/hosts/` files  
2. Switch to project's directory
3. Change variables in `/credentials`  
4. Crypt password via `mkpasswd --method=sha-512`  
5. change ip in `Vagrantfile` (optional)  
6. change to `ansible.playbook = "deployment/initial.yml"` in `Vagrantfile`  
7. `vagrant up`  
8. uncomment in `Vagrantfile` 
`config.vm.synced_folder ".", "/var/webapps/girls_proj/code", owner: "mtas_user", group: "users"`
- change to `ansible.playbook = "deployment/deploy.yml"`  
- `vagrant reload && vagrant provision`  
9. SSH to virtual server:  
   `vagrant ssh`


Initial remote server setup
---------------------------
1. Set absolute paths in `deployment/hosts/` files 
2. Switch to project's directory 
3. Change variables in `/credentials`  
4. Crypt password via `mkpasswd --method=sha-512`
5. Edit `deployment/vars.yml` file. Pay attention to `server_hostname`, `project_repo` and `remote_host` variables

#### To be continued
#### This configuration tested on Vagrant but for real remote i will test it soon
