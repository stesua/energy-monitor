# Overview
This project aim to collect tool to collect data from home power meter.

Components:
- Power meter: ORNO WE-515
- RS485 converter
- Python library
- InfluxDB
- Grafana



## Docker on raspberry
Must select images that are compatible with armv7l architecture (armv7 for 32 bit, armv8 for 64 bit)
Raspberry 3 should be processor:BCM2710, ARM_core:Cortex-A53, arm64, 64 bit


### Image compatibility

| Image     | armv7  | armv8      |
| --------- | ------ | ---------- |
| InfluxDB  | 1.8.10 | 2.5-alpine |
| Grafana   | 9.2.6  | 9.2.6      |


### Install
Install docker only: https://phoenixnap.com/kb/docker-on-raspberry-pi
```
sudo apt-get update && sudo apt-get upgrade
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh

# for example use pi as user_name
sudo usermod -aG docker [user_name]

# logout & login again (a reboot may be needed)

# enable docker at login (needed?)
sudo systemctl enable docker

# check docker service status
systemctl status docker.service

docker version
docker info
```

Already included in docker ~~Install docker and docker-compose: https://jfrog.com/connect/post/install-docker-compose-on-raspberry-pi/~~


## References
* [Docker-compose influxdb and grafana](https://github.com/jkehres/docker-compose-influxdb-grafana/blob/master/docker-compose.yml)