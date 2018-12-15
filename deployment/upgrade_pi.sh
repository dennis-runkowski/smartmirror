#!/usr/bin/env bash
set -e

sudo rm -rf /tmp/package

mkdir /tmp/package

cd /tmp/package

curl -LOk https://github.com/denrun-p/smartmirror/archive/master.zip
unzip -q master.zip && mv -f smartmirror-master smartmirror

rsync -r smartmirror/* /srv/smartmirror/
sudo rm -rf /tmp/package

# Ensure permissions
sudo chown -R pi:smartmirror /srv/

echo "###############################"
echo " Installing Python Packages"
echo "###############################"

# source virtualenv
source /srv/virtualenv/bin/activate

cd /srv/smartmirror
pip install -r requirements.txt
cd /srv/smartmirror/deployment

# Ensure permissions again for safety
sudo chown -R pi:smartmirror /srv/
sudo chmod -R g+rwx /srv/

echo "###################################"
echo "Completed!"
echo "Run the following to start the app:"
echo "sudo systemctl start emperor.uwsgi"
echo "###################################"

sudo reboot