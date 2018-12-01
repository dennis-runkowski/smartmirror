#!/bin/bash
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
echo "Deploying SmartMirror Application"
echo "###############################"


echo "##################################"
echo " Install Complete - Reboot the Pi"
echo "##################################"

echo "Some help commands below:"
echo "sudo nginx -t"
echo "sudo systemctl start|stop|restart emperor.uwsgi"
echo "source /srv/virtualenv/bin/activate "