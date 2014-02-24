#!/bin/sh -e

apt-get update

# build environment
apt-get -y install gcc build-essential python-dev git

# python
apt-get -y install python-pip python-virtualenv
cd /vagrant && virtualenv . && source bin/activate && pip install -r requirements.txt

# golang
wget https://go.googlecode.com/files/go1.2.linux-amd64.tar.gz
tar -C /usr/local -xzf go1.2.linux-amd64.tar.gz
echo "export PATH=$PATH:/usr/local/go/bin" >> /home/vagrant/.bash_profile

