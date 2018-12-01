#!/bin/bash
set -e
curl -LOk https://github.com/denrun-p/smartmirror/archive/master.zip
unzip master.zip && mv smartmirror-master smartmirror

cd smartmirror-master/deployment/raspberry_pi_config/
./raspberry_pi_install.sh

cd ../
./build.sh

timestamp=$(date +%s)

echo "###############################"
echo "Stopping the uWsgi Service"
echo "###############################"

sudo systemctl stop emperor.uwsgi

echo "###############################"
echo " Installing ...."
echo "###############################"

package_name=$(ls ./package/build* -Art | tail -n 1)
cd /tmp/package && tar -zxvf $package_name
cd /tmp/package && rsync -r smartmirror/* /srv/smartmirror/
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
echo "###################################"
echo " Restarting nginx and uwsgi emperor"
echo "###################################"

sudo systemctl daemon-reload
sudo systemctl enable nginx emperor.uwsgi
sudo systemctl restart nginx

echo "###################################"
echo "Completed!"
echo "Run the following to start the app:"
echo "sudo systemctl start emperor.uwsgi"
echo "###################################"

cd /srv/smartmirror
python smartmirror_setup.py