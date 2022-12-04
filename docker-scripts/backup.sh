#!/bin/sh

influxdb_backup() {
  date_path=$(date '+%Y-%m-%d_%H-%M-%S.%s')
  echo "$date_path"
  influx backup \
    "/home/influxdb/backups/$date_path" \
    -t="$DOCKER_INFLUXDB_INIT_ADMIN_TOKEN"
}

rotate_backups() {
  versions_to_keep=$1
  ls -1 -d /home/influxdb/backups/** | sort -r | awk "NR>$versions_to_keep" | xargs -t rm -r
}


cloud_storage_sync() {
  echo "Not implemented"
  return 1
}

influxdb_backup
rotate_backups 10