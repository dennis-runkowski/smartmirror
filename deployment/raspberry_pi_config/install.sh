#!/bin/bash
set -e

mkdir -p /srv

curl -LOk https://github.com/denrun-p/smartmirror/archive/master.zip
unzip master.zip && mv -f smartmirror-master smartmirror

mv -f smartmirror /srv/

cd /srv/smartmirror/deployment/raspberry_pi_config/
./raspberry_pi_install.sh

# Ensure permissions
sudo chown -R pi:smartmirror /srv/

cd /srv/smartmirror
python smartmirror_setup.py