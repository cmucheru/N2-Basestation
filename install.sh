sudo apt-get update && sudo apt-get -y upgrade
# sudo dpkg-reconfigure tzdata
sudo apt install -y nodejs npm python3-dev python3-venv virtualenv libffi-dev libssl-dev python3 python3-pip vim

curl -sSL https://get.docker.com | sh
sudo usermod -aG docker ${USER}
pip3 install docker-compose paho-mqtt numpy flask pyserial
mkdir Nakuja
cd Nakuja 
git clone https://github.com/nakujaproject/n2Basestation

sudo reboot
