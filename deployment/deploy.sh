#!/bin/bash

# Deploys the latest package to /tmp/package

set -e

echo "#####################################"
echo "Deploy Latest Smart Mirror package...."
echo "#####################################"

ssh_config=$1

if [ -z "$ssh_config" ]
then
	echo "Please add your ssh config i.e ./build SSH_CONFIG_NAME"
	exit 1
else
	echo ""
	echo "Deploying to $ssh_config"
	echo ""
fi

echo "#####################################"
echo " Grabbing Latest package...."
echo "#####################################"

package_name=$(ls ./packages -Art | tail -n 1)

echo ""
echo $package_name
echo ""

ssh -t $ssh_config 'sudo rm -rf /tmp/package'
ssh -t $ssh_config 'mkdir /tmp/package'

scp packages/$package_name $ssh_config:/tmp/package
scp install.sh $ssh_config:/tmp/package

echo ""
echo "#################################################"
echo "Complete!"
echo "Package $package_name is loacted in /tmp/package"
echo "Run ./tmp/package/install.sh to install"
echo "#################################################"