#!/bin/sh -e

apt-get update

# build environment
apt-get -y install gcc build-essential git

# golang
wget https://code.google.com/p/go/downloads/detail?name=go1.2.linux-amd64.tar.gz&can=2&q=
tar -C /usr/local -xzf go1.2.linux-amd64.tar.gz
echo -e "export GOROOT=$HOME/go\nexport PATH=$PATH:$GOROOT/bin" >> /home/vagrant/.bash_profile

