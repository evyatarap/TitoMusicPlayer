#!/bin/bash

SRC_INSTALLATION_DIR=`dirname $0`
DEST_INSTALLATION_DIR="/usr/local/bin/TitoControlService"
APP_LOG_DIR="/var/log/TitoControlService"

# install pip requirements
sudo pip3 install -r requirements.txt

# create service directories
if [! -d $DEST_INSTALLATION_DIR ] 
then
    sudo mkdir $DEST_INSTALLATION_DIR
fi

if [! -d $APP_LOG_DIR ]
then
    sudo mkdir $APP_LOG_DIR
fi

# copy files
sudo cp -r $SRC_INSTALLATION_DIR/* $DEST_INSTALLATION_DIR

# install as service
sudo cp $SRC_INSTALLATION_DIR/tito-control-service.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable tito-control-service.service
sudo systemctl restart tito-control-service.service
