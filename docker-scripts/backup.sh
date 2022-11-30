#!/bin/sh

influxdb_backup() {
  date_path=$(date '+%Y-%m-%d_%H-%M')
  echo "$date_path"
  influx backup \
    "/home/influxdb/backups/$date_path" \
    -t="$DOCKER_INFLUXDB_INIT_ADMIN_TOKEN"
}

cloud_storage_sync() {
  echo "Not implemented"
  return 1
}

influxdb_backup