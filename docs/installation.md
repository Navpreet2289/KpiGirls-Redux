Installation
============

Starting development
--------------------

Initial requirements:  

* `VirtualBox`  
* `Vagrant`  
* `Ansible`   
* Download `VBoxGuestAdditions.iso` for your version of VirtualBox


Steps to start development from command line:

1. Remove `172.16.0.39` from the `~/.ssh/known_hosts` (otherwise error can occur during provision);
2. Set absolute paths in `deployment/hosts/` files  
3. Switch to project's directory;
4. Start vagrant:  
   `vagrant up`  
5. Make a provision of project:  
   `ansible-playbook deployment/provision.yml -i deployment/hosts/development`
6. Uncomment this line in Vagrantfile to allow syncing a project directory:  
   `config.vm.synced_folder ".", "/var/webapps/girls_proj/code",owner: "mtas_user", group: "users"`
7. Now you have to reload vagrant, to sync your project directory with virtual server:  
   `vagrant reload` 
9. Make a deploy of project:  
   `ansible-playbook deployment/deploy.yml -i deployment/hosts/development`
10. SSH to virtual server:  
   `vagrant ssh`
11. Switch to project user:  
   `sudo su -l citymetrix_dev`
12. Create website superuser with username `admin` and password `admin` for convention:  
   `/var/webapps/citymetrix/virtualenv/bin/python /var/webapps/citymetrix/code/manage.py createsuperuser`
13. Freeze installed python packages in requirements.txt file:  
    `/var/webapps/citymetrix/virtualenv/bin/pip freeze > /var/webapps/citymetrix/code/requirements.txt`
14. Start django development server:  
    `/var/webapps/citymetrix/virtualenv/bin/python /var/webapps/citymetrix/code/manage.py runserver 0.0.0.0:8001`
15. Now you can see your app running in browser:  
    `http://127.0.0.1:8002/`


Initial remote server setup
---------------------------
1. Add files:  
   `credentials/production/super_user_name`  
   `credentials/production/super_user_password`  
   `credentials/production/super_user_password_crypted`  
   `credentials/production/project_user_name`  
   `credentials/production/project_user_password`  
   `credentials/production/project_user_password_crypted`  
   `credentials/production/ssh_port`  
   `deployment/hosts/initial`  
   `deployment/hosts/production`  
2. Edit `deployment/vars.yml` file. Pay attention to `server_hostname`, `project_repo` and `remote_host` variables
3. Generate `id_rsa` ssh key in `deployment/files/ssh/` directory by command (it asks you where to generate key):  
   `ssh-keygen -t rsa -C "yourmail@gmail.com"`  
4. Add public key `id_rsa.pub` in your repository, to allow server pull this repository.  
   This command can help:  
   `cat deployment/files/ssh/id_rsa.pub | pbcopy`
5. Do initial provision of server:  
   `ansible-playbook deployment/initial.yml -i deployment/hosts/initial --ask-pass -c paramiko` 
6. Update system packages and upgrade them if needed:  
   `ansible-playbook deployment/upgrade.yml -i deployment/hosts/production -K`  
7. Do project provision of server:  
   `ansible-playbook deployment/provision.yml -i deployment/hosts/production -K`  
9. Make first deploy of project:  
   `ansible-playbook deployment/deploy.yml -i deployment/hosts/production -K`
10. Login on remote server and create superuser;



Useful commands
---------------
`vagrant ssh`  
`sudo su -l mtas_user`  
`/var/webapps/girls_proj/virtualenv/bin/python /var/webapps/girls_proj/code/manage.py createsuperuser`  
`/var/webapps/girls_proj/virtualenv/bin/python /var/webapps/girls_proj/code/manage.py shell`  
`/var/webapps/girls_proj/virtualenv/bin/python /var/webapps/girls_proj/code/manage.py runserver 0.0.0.0:8001`  

`/var/webapps/girls_proj/virtualenv/bin/pip install <package>`  
`/var/webapps/girls_proj/virtualenv/bin/pip freeze > /var/webapps/girls_proj/code/requirements.txt`

`sudo locale-gen ru_RU.UTF-8`  
`sudo locale-gen en_US.UTF-8`


Passwords crypt
---------------
`>>> openssl passwd -salt salty -1 mypass`
`>>> mkpasswd --method=sha-512`