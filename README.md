# Overview
This project aim to collect tool to collect data from home power meter.

Components:
- Power meter: ORNO WE-515
- USB RS485 converter
- Python library
- InfluxDB
- Grafana

## Requirements
- raspberry 3+ with 64 bit OS (32 bit should work adjusting docker image versions)
- docker
- python 3.9 (TODO: evaluate support for previous version or adopt 3.11 instead)
- [poetry](https://python-poetry.org/docs/) for dev
- pip on raspberry

### Install poetry
```
curl -sSL https://install.python-poetry.org | python3 -
```

### Useful commands
```
# export requrirements
poetry export -f requirements.txt --output requirements.txt

pip install -r requirements.txt
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


## References
- [Docker-compose influxdb and grafana](https://github.com/jkehres/docker-compose-influxdb-grafana/blob/master/docker-compose.yml)
- TODO: add inspiring repo and documentations
- https://orno.pl/en/product/1079/1-phase-multi-tariff-energy-meter-wtih-rs-485-100a-mid-1-module-din-th-35mm
- https://b2b.orno.pl/download-resource/26063/ RS485 documentation

??? https://www.elocal.it/Soluzione.php?Usare-la-seriale-RS485-su-Raspberry-PI-3B

should be recognized already?
[    9.754441] usbcore: registered new interface driver ch341
[    9.754579] usbserial: USB Serial support registered for ch341-uart
[    9.754801] ch341 1-1.5:1.0: ch341-uart converter detected
[    9.758079] usb 1-1.5: ch341-uart converter now attached to ttyUSB0


## TODO
Add system service like https://github.com/fargiolas/we515mqtt/blob/master/we515mqtt.service


