import logging

from influxdb_client import InfluxDBClient
from influxdb_client.client.write_api import SYNCHRONOUS

from energy_collector.collect import Measure


class InfluxDBService:
    def __init__(self, org: str, bucket: str, url: str, token: str):
        self.org = org
        self.bucket = bucket
        self.url = url
        self.client = InfluxDBClient(url=url, token=token, org=org)
        self.write_api = self.client.write_api(write_options=SYNCHRONOUS)

    def write_measure(self, measure: Measure):
        logging.debug(f"Sending measure to influxDB {measure}")
        # TODO: improve it
        # FIXME: force to use float
        self.write_api.write(
            bucket=self.bucket,
            org=self.org,
            record=measure,
            record_measurement_key="name",
            record_time_key="timestamp",
            record_field_keys=[
                "frequency",
                "voltage",
                "current",
                "active_power",
                "reactive_power",
                "apparent_power",
                "power_factory",
            ])
