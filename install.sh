#!/bin/bash
# TODO: install all the other requirements if needed, like docker, python3, pip, envsubst
set -e

echo "init docker"
sudo systemctl enable docker
sudo systemctl start docker.service

echo "install services"
echo "installing energy-monitor-collector.service"
sudo sh -c 'envsubst < systemd-services/energy-monitor-collector.service > /etc/systemd/system/energy-monitor-collector.service'
sudo chmod 644 /etc/systemd/system/energy-monitor-collector.service
sudo systemctl daemon-reload
sudo systemctl enable energy-monitor-collector.service
sudo systemctl restart energy-monitor-collector.service
echo "energy-monitor-collector.service installed"

echo "installing energy-monitor-backup.service"
sudo cp systemd-services/energy-monitor-backup.service /etc/systemd/system/energy-monitor-backup.service
sudo chmod 644 /etc/systemd/system/energy-monitor-backup.service
sudo systemctl daemon-reload
sudo systemctl enable energy-monitor-backup.service
echo "energy-monitor-backup.service installed"

echo "installing energy-monitor-backup.timer"
sudo cp systemd-services/energy-monitor-backup.timer /etc/systemd/system/energy-monitor-backup.timer
sudo chmod 644 /etc/systemd/system/energy-monitor-backup.timer
sudo systemctl daemon-reload
sudo systemctl enable energy-monitor-backup.timer
sudo systemctl start energy-monitor-backup.timer
echo "energy-monitor-backup.timer installed"

# FIXME: either copy config and mounted folder here or change strategy (maybe with pipenv will work)
#echo "installing energy-monitor-influxdb-grafana.service"
#sudo sh -c 'envsubst < systemd-services/energy-monitor-influxdb-grafana.service > /etc/systemd/system/energy-monitor-influxdb-grafana.service'
#sudo chmod 644 /etc/systemd/system/energy-monitor-influxdb-grafana.service
#sudo systemctl daemon-reload
#sudo systemctl enable energy-monitor-influxdb-grafana.service
#sudo systemctl start energy-monitor-influxdb-grafana.service
#echo "energy-monitor-influxdb-grafana.service installed"

# install python dependencies
echo "installing energy collector python requirements"
cd energy-collector || echo "Cannot find energy-collector directory" || exit 1
pipenv install
cd ..
echo "energy collector python requirements installed"




