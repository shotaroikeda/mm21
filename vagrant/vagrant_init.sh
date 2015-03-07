#!/usr/bin/env bash

apt-get -y update
apt-get -y install ubuntu-desktop
apt-get -y install pip
apt-get -y install vim
pip install python-pygame
startx
