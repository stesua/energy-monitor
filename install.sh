#!/bin/bash
# init docker
sudo systemctl enable docker
sudo systemctl start docker.service

# install services
sudo sh -c 'envsubst < systemd-services/energy-monitor-collector.service > /etc/systemd/system/energy-monitor-collector.service'
sudo chmod 644 /etc/systemd/system/energy-monitor-collector.service
sudo systemctl daemon-reload
sudo systemctl enable energy-monitor-collector.service
sudo systemctl start energy-monitor-collector.service

sudo cp systemd-services/energy-monitor-backup.service /etc/systemd/system/energy-monitor-backup.service
sudo chmod 644 /etc/systemd/system/energy-monitor-backup.service
sudo systemctl daemon-reload
sudo systemctl enable energy-monitor-backup.service

sudo cp systemd-services/energy-monitor-backup.timer /etc/systemd/system/energy-monitor-backup.timer
sudo chmod 644 /etc/systemd/system/energy-monitor-backup.timer
sudo systemctl daemon-reload
sudo systemctl enable energy-monitor-backup.timer
sudo systemctl start energy-monitor-backup.timer

# FIXME: either copy config and mounted folder here or change strategy
#sudo sh -c 'envsubst < systemd-services/energy-monitor-influxdb-grafana.service > /etc/systemd/system/energy-monitor-influxdb-grafana.service'
#sudo chmod 644 /etc/systemd/system/energy-monitor-influxdb-grafana.service
#sudo systemctl daemon-reload
#sudo systemctl enable energy-monitor-influxdb-grafana.service
#sudo systemctl start energy-monitor-influxdb-grafana.service

# install python dependencies
cd energy-collector || echo "Cannot find energy-collector directory" || exit 1
pip install -r requirements.txt
cd ..




