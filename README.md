# Overview
This project goal is to collect data from home power meter, it's intended for home use only and requires professional electrician support to install the required hardware since it could be potentially lethal. 

The vision of this project is to be able to categorize energy consumption into the corresponding device using a machine learning model, this particular use case it's still at an early stage.

This project is not mature yet and could be changed in non-backward compatible manner in feature versions. 

## Features
- Metric collector python script
  - configurable with different hardware interface
  - 1s collection rate
  - installed as systemd service
- Time series database using influxdb
  - provisioned into docker
  - automatic backup every 1 hour using systemd service
  - backup rotation to keep only latest 10 run using systemd service
- Visualization using grafana
  - provisioned into docker
  - built-in ready to use dashboard
- Install
  - automatic install script

## Components:
- Raspberry 3B+
- Power meter used is [ORNO WE-515](https://www.partner.orno.pl/manuals/OR-WE-512,514,515_manual_EN.pdf) but should be easily replaced with similar product that support RS485 standard 
- USB RS485 converter
- Python library to collect measure and send to the time series database
- InfluxDB to store collected measure
- Grafana to visualize measure


## Requirements
- Raspberry 3+ with 64 bit OS (32 bit should work adjusting docker image versions)
- Docker
- Python 3.9
- [Poetry](https://python-poetry.org/docs/) for development environemnt
- Pip on raspberry

### Install poetry
```
curl -sSL https://install.python-poetry.org | python3 -
```

### Useful commands
```
# export requrirements
poetry export -f requirements.txt --output requirements.txt

# install requirements on raspberry
pip install -r requirements.txt

# run in background
nohup python energy_collector/app.py &

# check services
sudo systemctl status energy-monitor*

# check systemctl logs
journalctl -u energy-monitor-collector.service
journalctl -u energy-monitor-backup.service
```


## Docker on raspberry
Must select images that are compatible with armv7l architecture (armv7 for 32 bit, armv8 for 64 bit)
Raspberry 3 should be processor:BCM2710, ARM_core:Cortex-A53, arm64, 64 bit


### Image compatibility

| Image     | armv7  | armv8      |
| --------- | ------ | ---------- |
| InfluxDB  | 1.8.10 | 2.5-alpine |
| Grafana   | 9.2.6  | 9.2.6      |


### Install
Install docker (recent version includes docker compose): https://phoenixnap.com/kb/docker-on-raspberry-pi
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

## InfluxDB
```
# create local development env influx cli configuration
influx config create \
  -n local \
  -u http://localhost:8086 \
  -p admin:admin123 \
  -o home
  
# create raspberry development env influx cli configuration
RASBERRY_IP=192.168.1.248 influx config create \
  -n raspberry \
  -u "http://$RASPBERRY_IP:8086" \
  -p admin:admin123 \
  -o home
  
influx backup ./influxdb-backups/[local|raspberry]/$(date '+%Y-%m-%d_%H-%M') -t influx-db-token

# drop data with time and measurement filters
influx delete \
  --bucket energy \
  --start 1970-01-01T00:00:00Z \
  --stop $(date +"%Y-%m-%dT%H:%M:%SZ") \
  --predicate '_measurement="energy"'
  
# restore backup
influx config [local|raspberry]
influx bucket delete -n energy -t influx-db-token
influx restore influxdb-backups/2022-12-02_18-15 -t influx-db-token
```


## Troubleshooting
Locale not set warning (https://daker.me/2014/10/how-to-fix-perl-warning-setting-locale-failed-in-raspbian.html):
```shell
perl: warning: Setting locale failed.
perl: warning: Please check that your locale settings:
	LANGUAGE = (unset),
	LC_ALL = (unset),
	LC_CTYPE = "UTF-8",
	LC_TERMINAL = "iTerm2",
	LANG = "en_US.UTF-8"
    are supported and installed on your system.
```
solve it by running:
```shell
export LANGUAGE=en_US.UTF-8
export LANG=en_US.UTF-8
export LC_ALL=en_US.UTF-8
sudo locale-gen en_US.UTF-8
```

## References
- [Docker-compose influxdb and grafana](https://github.com/jkehres/docker-compose-influxdb-grafana/blob/master/docker-compose.yml)
- TODO: add inspiring repo and documentations
- https://orno.pl/en/product/1079/1-phase-multi-tariff-energy-meter-wtih-rs-485-100a-mid-1-module-din-th-35mm
- https://b2b.orno.pl/download-resource/26063/ RS485 documentation

??? https://www.elocal.it/Soluzione.php?Usare-la-seriale-RS485-su-Raspberry-PI-3B


## TODO
- add measure of active and reactive energy 
- refactor energy measure into main since in general with different power meter or power sensor you can collect different measurement 
  - BREAKING CHANGE! (preserve data by backup and restore smartly)
- move backup into cloud
- export data for analytics and ML purpose
- compute price by interpolating energy and price at a given time
- create terraform resource for azure (then gcs and aws)
- add raspberry metrics, like cpu usage, memory, temperature ...- 
- monitor raspberry pi metrics with influxdb + telegraf https://randomnerdtutorials.com/monitor-raspberry-pi-influxdb-telegraf/
- check influxdb memory usage 
  - try increase swap memory: https://pimylifeup.com/raspberry-pi-swap-file/ 
- install script should restart docker services to make new file available there as well (NB: restart grafana and influxdb not docker)
- install script should install all requirements pip, python3.9, docker, envsubst ...
- add test coverage
- add CI/CD (choose the tool, github actions/circleci...)
- add alerts for power overload
- add alerts in case of issue in collecting
- add python linter and pre-commit hook 
 
