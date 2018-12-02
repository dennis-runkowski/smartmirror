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
echo " Setting up uwsgi and nginx config"
echo "###################################"

# uwsgi config
sudo mv /srv/smartmirror/deployment/uwsgi_emperor/emperor.uwsgi.service /etc/systemd/system/
sudo mv /srv/smartmirror/deployment/uwsgi_vassals/uwsgi_app.ini /etc/uwsgi-emperor/vassals/

# nginx
sudo mv /srv/smartmirror/deployment/nginx/smartmirror /etc/nginx/sites-available/
set +e
sudo ln -s /etc/nginx/sites-available/smartmirror /etc/nginx/sites-enabled
set -e

cd /srv/smartmirror
python smartmirror_setup.py

echo "###################################"
echo " Restarting nginx and uwsgi emperor"
echo "###################################"

sudo systemctl daemon-reload
sudo systemctl enable nginx emperor.uwsgi
sudo systemctl restart nginx


