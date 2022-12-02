#!/bin/bash
# init docker
sudo systemctl enable docker
sudo systemctl start docker.service

# install services
sudo sh -c 'envsubst < systemd-services/energy-collector.service > /etc/systemd/system/energy-collector.service'
sudo chmod 644 /etc/systemd/system/energy-collector.service
sudo systemctl daemon-reload
sudo systemctl enable energy-collector.service
sudo systemctl start energy-collector.service

sudo cp systemd-services/influx-db-backup.service /etc/systemd/system/influx-db-backup.service
sudo chmod 644 /etc/systemd/system/influx-db-backup.service
sudo systemctl daemon-reload
sudo systemctl enable influx-db-backup.service

sudo cp systemd-services/influx-db-backup.timer /etc/systemd/system/influx-db-backup.timer
sudo chmod 644 /etc/systemd/system/influx-db-backup.timer
sudo systemctl daemon-reload
sudo systemctl enable influx-db-backup.timer
sudo systemctl start influx-db-backup.timer

sudo sh -c 'envsubst < systemd-services/influx-db-grafana.service > /etc/systemd/system/influx-db-grafana.service'
sudo chmod 644 /etc/systemd/system/influx-db-grafana.service
sudo systemctl daemon-reload
sudo systemctl enable influx-db-grafana.service
sudo systemctl start influx-db-grafana.service

# install python dependencies
cd energy-collector || echo "Cannot find energy-collector directory" || exit 1
pip install -r requirements.txt
cd ..




