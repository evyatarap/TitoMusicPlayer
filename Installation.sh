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