# Install mopidy
wget -q -O - https://apt.mopidy.com/mopidy.gpg | sudo apt-key add -
sudo wget -q -O /etc/apt/sources.list.d/mopidy.list https://apt.mopidy.com/buster.list
sudo apt update
sudo apt install mopidy

# Setup mopidy as a service
sudo systemctl enable mopidy
sudo systemctl start mopidy

# Installing spotify plugin
sudo apt install mopidy-spotify
sudo systemctl restart mopidy

# Install python-pip
sudo apt-get install python3-pip

# Install a simple mopidy web-client
sudo python3 -m pip install Mopidy-MusicBox-Webclient

# Enable SPI by running raspi-config (or uncomment the 'dtparam=spi=on' on /boot/config.txt)
## Requires reboot
sudo raspi-config

# Installing SPI python library
sudo apt-get install python2.7-dev

git clone https://github.com/lthiery/SPI-Py.git
cd SPI-Py
sudo python setup.py install

# Installing RFID-RC522 python library
git clone https://github.com/mxgxw/MFRC522-python.git

# Installing python2.7 pip
sudo apt-get install python-pip
pip3 install spidev
pip3 install pi-rc522

git clone https://github.com/ondryaso/pi-rc522.git

# Install speach library
sudo apt-get install espeak

# reboot pi to enable SPI settings
sudo reboot