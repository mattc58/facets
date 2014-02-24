#!/bin/sh -e

apt-get update

# build environment
apt-get -y install gcc build-essential git

# python
apt-get -y install python-pip python-virtualenv

# golang
wget https://go.googlecode.com/files/go1.2.linux-amd64.tar.gz
tar -C /usr/local -xzf go1.2.linux-amd64.tar.gz
echo "export PATH=$PATH:/usr/local/go/bin" >> /home/vagrant/.bash_profile

