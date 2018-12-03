#!/usr/bin/env bash
set -e

echo "_____________________________________________________________________________________________________________________________________"

echo "  #######                                                   ######       ######"
echo " #########                                                  #######     ####### "
echo " ###   ###                                                  ########   ######## "
echo " ###   ###                                                  ###  #########  ### "
echo " ###   ###                                                  ###   #######   ###"
echo " ###                                                        ###    #####    ###"
echo "  ###                                                       ###     ###     ###"
echo "    ###                                                     ###             ###                                                     "
echo "      ###                                                   ###             ###                                                     "
echo "        ###  ######    ######  #######  ######### ######### ###             ### ### #########    #########     #######   #########"
echo "         ### #######  ####### ######### ######### ######### ###             ### ### #########    #########    #########  #########"
echo " ###     ### ################ ###   ### ###   ###    ###    ###             ### ### ###   ###    ###   ###   ###     ### ###   ###"
echo " ###     ### ###  ######  ### ######### #########    ###    ###             ### ### #########    #########   ###     ### #########"
echo " ###     ### ###   ####   ### ######### ###   ###    ###    ###             ### ### ###    ###   ###    ###  ###     ### ###    ###"
echo " ########### ###          ### ###   ### ###    ###   ###    ###             ### ### ###     ###  ###     ###  #########  ###     ###"
echo "  #########  ###          ### ###   ### ###     ###  ###    ###             ### ### ###      ### ###      ###  #######   ###      ###"

echo "______________________________________________________________________________________________________________________________________"

echo " "

echo "Installing the SmartMirror on your pi will make changes to the raspberry configurations."
echo "Do you want to continue with the install (y/n):"

read install

if [ "$install" == "y" ]; then
    echo "install"
else
    echo "Stopping the installation!"
    exit 1
fi

sudo apt-get update && sudo apt-get upgrade

mkdir -p /srv

curl -LOk https://github.com/denrun-p/smartmirror/archive/master.zip
unzip -q master.zip && mv -f smartmirror-master smartmirror

mv -f smartmirror /srv/

sudo apt-get update && sudo apt-get upgrade

# Create group
sudo getent group smartmirror || addgroup smartmirror
sudo adduser pi smartmirror
sudo adduser www-data smartmirror

# Creating logging directories
sudo mkdir -p /var/log/smartmirror
sudo mkdir -p /srv/smartmirror
sudo chown -R www-data:www-data /var/log/smartmirror
sudo chown -R pi:smartmirror /srv/
sudo chmod -R g+rwx /srv/

mkdir -p /home/pi/.config/lxsession
mkdir -p /home/pi/.config/lxsession/LXDE-pi

sudo rm -f /home/pi/.config/lxsession/LXDE-pi/autostart
sudo mv autostart /home/pi/.config/lxsession/LXDE-pi/

echo "###################################"
echo " Installing Virtualenv and Wrapper"
echo "###################################"

pip install virtualenv
virtualenv /srv/virtualenv

echo "###############################"
echo " Installing Nginx"
echo "###############################"

sudo apt-get install nginx

echo "###############################"
echo " Installing uWsgi"
echo "###############################"

sudo apt-get install uwsgi-emperor uwsgi
sudo apt-get install uwsgi-plugin-python

echo "###############################"
echo " Installing Sqlite"
echo "###############################"

sudo apt-get install sqlite

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

#Ensure permissions
sudo chown -R pi:smartmirror /srv/
sudo chmod -R g+rwx /srv/

echo "##################################"
echo "Install and Setup is finished"
echo "##################################"

echo "Do you want to reboot the pi now (y/n):"
read reboot

if [ "$reboot" == "y" ]; then
    sudo reboot
else
    exit 1
fi