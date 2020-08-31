[![Build Status](https://build.spottmedia.com/buildStatus/icon?job=ansible_role_nvm_node)](https://build.spottmedia.com/buildStatus/icon?job=ansible_role_nvm_node)

# Ansible NVM Node

Installs node via NVM on Debians and Redhats.

## installation ##

either
* `ansible-galaxy install grzegorznowak.nvm_node`
* clone the repo directly

## Dislaimer ## 
It's a pretty bespoke installation of node that doesn't rely on any of apt/yum goodies 
nor it follows the *recommended* (@see https://github.com/creationix/nvm/issues/1533) way of using NVM.
Additionally versioning is only achievable via Ansible itself. 
Please make sure the setup given here is the one you actually do require on your end.
I would say it's __70%__ for DEV purposes and __30%__ for live. 
And __0%__ if you plan having many users/roles using it on a single server - it's not going to fly in the current state 
(though might work at some point with relatively minimal extra love added).

The crux is it installs nvm into a global path and symlinks it back to `/usr/local/bin` for general accessibility, and hijacks global bashrc to include the NVM's paths for each user on the system.
Which although minor, breaks the concept of VNM being a per-user tool, as well as not working 100% flawlessly when specific non-interactive shells are used. This might affect usage of npm installed packages for those cases.
__However__ a cool cat as it is, nvm really is the tool of our choice so that's the way we need it and might be you need it too!
 
## Requirements

No dependencies, just note it will install `wget` to fetch the nvm installation script.

## Coverage

Currently builds and integrates on those distros:

##### Ubuntu: 20.04, 18.04, 16.04, 14.04
##### Debian: buster, stretch
##### CentOS: 7  
 

## Variables

### defaults
```YAML
    nvm_install_script_version: "0.33.11"   # the nvm installation script to use (latest stable version as of writing this)
    nvm_user_name: "root"                   # you can use a different user, and you might in the end achieve the more nvm-ish approach
                                            # but I've not covered that in tests etc.  
    nvm_dir: "/var/lib/nvm"                 # for global (default) installation. Follow the same rule as the nvm_user_name variable
    nvm_node_version: "8.11.3"              # the node version to install via nvm
    nvm_install_globally: []                # libraries to intall globally and symlink, look further down for details
```      

## Example playbook 
##### when cloned from github
```YAML
    ---
    - hosts: all
      vars:
        nvm_node_version: "4.1.1"
      roles:
        - role: ansible-nvm-node
```        
##### when from ansible-galaxy

```YAML
    ---
    - hosts: all
      vars:
        nvm_node_version: "your.node.version"
      roles:
        - role: grzegorznowak.nvm_node        
```
## Upgrading node

Simply replace `nvm_node_version` with whatever version you want to be using globally and rerun the playbook


## Installing global packages

For the best coherency you are strongly encouraged to install global packages using this role too, in which case 
just edit the `nvm_install_globally` variable, as follows:

```YAML
nvm_install_globally: ['gulp']
```
also can use version targeting for global packages:

```YAML
nvm_install_globally:
  - name: yarn
    version: 1.9.4
```

or mix both:

```YAML
nvm_install_globally:
  - gulp
  - lighthouse
  - name: yarn
    version: 1.9.4
```

and that will install listed libraries and put a symlink to global $PATH 
for specific environments to access it (like cron)
 
## Testing

### Requirements

you may use a helper script that will install virtual env with all the needed stuff 
    `./bootstrap_test.sh`

the simply activate the virtualenv with `source test_env/bin/activate`

or just do it 100% manually for better control

    sudo apt install virtualenv python3-pip
    virtualenv test_env --python=python3
    source test_env/bin/activate
    pip install -r test-requirements.txt
    
### Testing with lxc containers

    molecule test

### Additional perks from molecule

You can do all sort of super handy stuff like `molecule converge` to simply bring instance(s) at will 
and then tear them down with `molecule destroy`. The sky is the limit here really!

## Sponsored by

#### [Kwiziq.com](https://www.kwiziq.com) - The AI language education platform
#### [Spottmedia.com](http://www.spottmedia.com) - Technology design, delivery and consulting


## Author Information

brought to you with love from [Grzegorz Nowak](https://www.linkedin.com/in/grzegorz-nowak-356b7360/).
