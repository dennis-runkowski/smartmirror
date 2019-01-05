![Alt text](img/SmartMirror.jpg?raw=true "Smartmirror")

`*Work in Progress*`

![Alt text](img/smartmirror.JPG?raw=true "Smartmirror")

## Table Of Contents
- [Overview](#Overview)
- [Requirements](#Requirements)
- [Raspberry Pi Install](#Raspberry-Pi-Install)
- [Configuring](#Configuring)
- [Local Setup](#Local-Setup)
- [Local Deployment](#Local-Deployment)
- [Updating](#Updating) 
- [Architecture](#Architecture)

## Overview
The SmartMirror application is a Python2.7 Flask app that breaks the screen into panels and banners. The application was designed to run on a raspberry pi 2/3 paired with a ~24 inch monitor. Panels and banners are just the section of the screen for the different plugins. For example you can configure the left panel to display the current weather. There are five sections that use a standardized naming convention, see below. I know this restricts the flexibility of the plugin location on the mirror, I am working on a drag and drop feature :smiley:.
* The top of the screen is called the `top_banner`
* The left side of the screen is called the `left_panel`
* The right side of the screen is split into two sections
    * There's the right top which is a smaller section used for the date/time `right_top_panel`
    * Then there's the right bottom which is a bit larger `right_bottom_panel`
* The last section is the bottom which is called the `bottom_banner`

Another common term in this application is `plugin`, these are the different components that can be configured like the weather, news or date/time.

The plugins that the SmartMirror uses are saved in the file config.yml. There are few ways to change the plugins the SmartMirror uses. For the nerds you can use the script smartmirror_setup.py, that will step you through the available plugins and save them to the config.yml. Or you can use the frontend route /setup. If you are running the app locally, install the requirements, execute `python run.py` and :boom: you are up and running. If you installed the app on your raspberry pi using the instructions below, you need to restart the flask app or reboot the pi to see the new plugins.

Read the architecture section for the application details.

## Requirements
Below are some links to the parts, but these are only recommendations! You can use cheaper parts, this is just what I had success with.
* Currently built for `linux operating systems` only (windows coming soon!)
* `Designed for a 24 inch monitor`
* `Python2.7`
* Basic Flask, Linux and Bash knowledge
* Raspberry Pi 2/3 (https://www.amazon.com/gp/product/B01C6Q2GSY/ref=oh_aui_search_detailpage?ie=UTF8&psc=1)
* Two way mirror (https://www.amazon.com/gp/product/B06Y2JMH7C/ref=oh_aui_detailpage_o00_s01?ie=UTF8&psc=1  )
* 24 inch in ultra thin monitor (https://www.amazon.com/gp/product/B01HIA63AU/ref=oh_aui_detailpage_o00_s00?ie=UTF8&psc=1)
* Frame to house the components

## Raspberry Pi Install
1. Make sure you change the default password to your pi for security reasons.
2. Setup ssh on you pi.
3. Install the pi by opening a terminal and running this command on your pi. Follow all the instructions during the installation.
```bash
sudo bash -c "$(curl -sL https://raw.githubusercontent.com/denrun-p/smartmirror/master/deployment/raspberry_pi_config/raspberry_pi_install.sh)"
```

## Configuring
PlaceHolder

### Local Setup
The SmartMirror application was made to be developer friendly. To get started setup a development environment on your local machine, follow the steps below:

**Clone/Download this repo to your local machine.**

**Ensure the correct python is installed:**
```
dennis_ubuntu@Dennis-Runkowski-Ubuntu:~$ python
Python 2.7.12 (default, Dec  4 2017, 14:50:18) 
[GCC 5.4.0 20160609] on linux2
Type "help", "copyright", "credits" or "license" for more information.
>>> 
```
**Ensure pip is installed (version doesn't matter):**
```
dennis_ubuntu@Dennis-Runkowski-Ubuntu:~$ pip --version
pip 9.0.1 from /home/dennis_ubuntu/.local/lib/python2.7/site-packages (python 2.7)

```
**Install virtualenv with pip and create a virtual environment in your project directory.**
```
pip install virtualenv
virtualenv smartmirror
source smartmirror/bin/active
```
**Install Python packages**
```
pip install -r requirements.txt
```
**Configure the smartmirror with plugins and credentials.**
```
(smart_mirror) dennis_ubuntu@Dennis-Runkowski-Ubuntu:~/GitHub/smartmirror$ python smartmirror_setup.py 
-----------------------------------
|                                 |
|        Smart Mirror Setup       |
|              v1.0.0             |
-----------------------------------
   
The smart mirror uses the follow
grid to display your desired plugins.
 
-----------------------------------
|           Top Banner            |
|                                 |
-----------------------------------
| Left   |               | R. Top |
| Panel  |               |--------|
|        |               | R.     |
|        |               | Bottom |
-----------------------------------
|           Bottom Banner         |
|                                 |
-----------------------------------
 
 
Do you want to use the testing configuration (y/n)?: y
Lets setup the Top Banner!
 
Do you want to use the Top Banner (y/n)?: y
These are the available plugins for the Top Banner:
1. Greetings
2. Quotes
3. Python Tips
4. Reminders

Please enter the plugin number (i.e. 1): 1
-----------------------------------
 
Lets setup the Left Panel!
 
Do you want to use the Left Panel (y/n)?: n
-----------------------------------
 
Lets setup the Right Top Panel!
 
Do you want to use the Right Top Panel (y/n)?: y
Currently there is only one plugin for this panel
 8. Date and Time

Please enter the plugin number (i.e. 1): 8
-----------------------------------
 
Lets setup the Right Bottom Panel!
 
Do you want to use the Right Bottom Panel (y/n)?: n
-----------------------------------
 
Lets setup the Bottom Banner!
 
Do you want to use the Bottom Banner (y/n)?: n

Saving your config to config.yml
Completed!

```
***Follow the steps in the smartmirror_setup.py script. I recommend starting with one or two plugins for the first run. For a deeper dive into the application see the `Application Details` section.***

## Local Deployment
Placeholder

## Updating
PlaceHolder

## Architecture
Placeholder


### TO DO
* Testing
* Additional logging
* Enhance documentaion and comments