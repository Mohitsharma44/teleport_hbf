set -eux

# Upgrade linux kernel
curl -fsSL https://raw.githubusercontent.com/pimlie/ubuntu-mainline-kernel.sh/master/ubuntu-mainline-kernel.sh -o ubuntu-mainline-kernel.sh
chmod +x ubuntu-mainline-kernel.sh
sudo bash ubuntu-mainline-kernel.sh -i 5.17.5 --yes
