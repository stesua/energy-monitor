#!/bin/bash

export PROJECT_PATH=$PWD

# init docker
sudo systemctl enable docker
sudo systemctl start docker.service

# install services
envsubst < systemd-services/energy-collector.service > /etc/systemd/system/energy-collector.service
sudo chmod 644 /etc/systemd/system/energy-collector.service
sudo systemctl daemon-reload
sudo systemctl enable energy-collector.service
sudo systemctl start energy-collector.service

cp systemd-services/influx-db-backup.service /etc/systemd/system/influx-db-backup.service
sudo chmod 644 /etc/systemd/system/influx-db-backup.service
sudo systemctl daemon-reload
sudo systemctl enable influx-db-backup.service
sudo systemctl start influx-db-backup.service

# install python dependencies
cd energy-collector || echo "Cannot find energy-collector directory" || exit 1
pip install -r requirements.txt
cd ..




