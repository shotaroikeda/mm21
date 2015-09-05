#!/usr/bin/env bash

# Java
add-apt-repository -y ppa:webupd8team/java
echo "oracle-java8-installer shared/accepted-oracle-license-v1-1 select true" | sudo debconf-set-selections
apt-get -y update
apt-get -y install oracle-java8-installer

# Game dependencies
apt-get -y update
apt-get -y install pip
apt-get -y install git
pip install pygame

# Desktop + Editors/IDEs
apt-get -y install vim
apt-get -y install emacs
apt-get -y install eclipse-platform
apt-get -y install ubuntu-desktop

# Useful dev tools
pip install flake8

# Game itself
mkdir ~/Desktop/mm21 && cd ~/Desktop/mm21
git init
git remote add origin https://github.com/acm-uiuc/mm21

# Eclipse instructions
# TODO Put on wiki
EG="~/Desktop/eclipse_guide.txt"
echo "" > $EG

echo "How to use Eclipse" >> $EG
echo "*** Check out the code (cd ~/Desktop/mm21 && git pull origin master) before starting this phase! ***" >> $EG
echo "1) Click the 'dash home' button at the top left of your screen" >> $EG
echo "2) Search for (and click on) Eclipse" >> $EG
echo "3) File > New Project (name it 'mm21' or something similar)" >> $EG
echo "4) Uncheck 'Use default location', and use '/root/Desktop/mm21/test-clients/java/' instead" >> $EG
echo "5) Click 'Finish'" >> $EG

# Go!
startx
