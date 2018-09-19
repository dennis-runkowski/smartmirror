# SmartMirror
`*Work in Progress*`

This tutorial will show you how to create your own smartmirror with a raspberry pi and a two way mirror. The smartmirror is powered by a raspberry pi running a flask application. The application is plugable with customed plugins to fit your needs.

![Alt text](img/smartmirror.JPG?raw=true "Smartmirror")

## Getting Started
These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. See deployment for notes on how to deploy the project on rasberry pi.
### Requirements
* Currently built for `linux operating systems` only (windows coming soon!)
* `Designed for a 24 inch monitor`
* `Python2.7`
* Basic Flask, Linux and Bash knownledge
* Raspberry Pi 3
* Two way mirror
* 24 inch in ultra thin monitor

### Local Setup
To quickly get started on your local machine, follow the steps below:

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

### Application Details
Placeholder

### Raspberry Pi Setup

Placeholder

### Deployment

### Physical Setup

Placeholder

### TO DO
* Testing
* Additional logging
* Enhance documentaion and comments