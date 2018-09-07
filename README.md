# SmartMirror
`*Work in Progress*`

This tutorial will show you how to create your own smartmirror with a raspberry pi and a one way mirror. The smartmirror is powered with a flask application that can be configured to your needs.
## Getting Started
These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. See deployment for notes on how to deploy the project on rasberry pi.

![Alt text](img/smartmirror.JPG?raw=true "Smartmirror")

### Requirements
* Currently built for `linux systems` only (windows coming soon!)
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

### Raspberry Pi Setup

Placeholder

### Deployment

### Application Details
Placeholder

### Physical Setup

Placeholder