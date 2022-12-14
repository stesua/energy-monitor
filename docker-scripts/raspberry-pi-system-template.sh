#!/bin/sh
set -e

config_path="/home/influxdb/configs"

export_influxdb_configs() {
  if [ -s "$config_path" ]
  then
    export "$(xargs < "$config_path")"
  fi
}

export_influxdb_configs

if [ -z "$STACK_ID" ]
then
  echo "Installing raspberry pi system monitor template"
  influx apply \
    -u https://raw.githubusercontent.com/influxdata/community-templates/master/raspberry-pi/raspberry-pi-system.yml \
    --force yes | tail -1 | sed 's/Stack ID: /STACK_ID=/g' > "$config_path"
  export_influxdb_configs
  echo "Raspberry pi system monitor template installed $STACK_ID"
else
  echo "Raspberry pi system monitor template already installed $STACK_ID, skipping"
fi

