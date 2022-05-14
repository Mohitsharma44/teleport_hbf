#!/bin/bash

set -eux

# bcc dependencies
sudo apt-get update
# sudo apt-get install -y bpfcc-tools "linux-headers-$(uname -r)" \
sudo apt-get install -y bpfcc-tools "linux-headers-$(uname -r)" \
  bison build-essential cmake flex git libedit-dev \
  libllvm7 llvm-7-dev libclang-7-dev python zlib1g-dev libelf-dev libfl-dev python3-distutils python3-pip

# Install docker
curl -fsSL https://get.docker.com -o get-docker.sh
sh get-docker.sh
sudo usermod -aG docker vagrant

curl -fsSL https://github.com/docker/compose/releases/download/v2.5.0/docker-compose-linux-x86_64 -o docker-compose
chmod +x docker-compose
sudo mv docker-compose /usr/local/bin/docker-compose

# Setup bcc
rm -rf bcc && git clone https://github.com/iovisor/bcc.git
cd bcc && git checkout v0.24.0 && cd ..
mkdir bcc/build; cd bcc/build
export LLVM_ROOT=/usr/lib/llvm-7
cmake ..
make
sudo make install
cmake -DPYTHON_CMD=python3 ..
pushd src/python/
make
sudo make install
popd

## Need to find a way to fix this...
sudo apt --fix-broken install