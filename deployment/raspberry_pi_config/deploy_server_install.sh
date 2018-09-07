#!/bin/bash

# Deploys the install script to /tmp/install

set -e

echo "##########################################"
echo "Deploy Latest Raspberry Pi install script"
echo "##########################################"

ssh_config=$1

if [ -z "$ssh_config" ]
then
	echo "Please add your ssh config i.e ./deploy_server_install.sh SSH_CONFIG_NAME"
	exit 1
else
	echo ""
	echo "Deploying to $ssh_config"
	echo ""
fi

ssh -t $ssh_config 'sudo rm -rf /tmp/install'
ssh -t $ssh_config 'mkdir /tmp/install'

scp autostart $ssh_config:/tmp/install
scp raspberry_pi_install.sh $ssh_config:/tmp/install

echo ""
echo "#################################################"
echo "Complete!"
echo "Run ./tmp/install/raspberry_pi_install.sh to install"
echo "#################################################"