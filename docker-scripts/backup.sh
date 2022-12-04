#!/bin/sh
set -e

influxdb_backup() {
  date_path=$(date '+%Y-%m-%d_%H-%M-%S.%s')
  echo "Backing up into $date_path"
  influx backup \
    "/home/influxdb/backups/$date_path" \
    -t="$DOCKER_INFLUXDB_INIT_ADMIN_TOKEN"
  echo "Backup completed"
}

rotate_backups() {
  echo "Rotating backups"
  versions_to_keep=$1
  ls -1 -d /home/influxdb/backups/** | sort -r | awk "NR>$versions_to_keep" | xargs -t rm -r
  echo "Rotate backups completed"
}

cloud_storage_sync() {
  echo "Not implemented"
  return 1
}

influxdb_backup
rotate_backups 10