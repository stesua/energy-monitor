import datetime
import logging
import sys

from collect import provide_smart_meter_collector
from influxdb import InfluxDBService
from timeloop import Timeloop
from datetime import timedelta, datetime

tl = Timeloop()


# TODO: configure interval
@tl.job(interval=timedelta(seconds=1))
def run_job():
    logging.debug(f"monitoring job triggered at {datetime.utcnow()}")
    token = "influx-db-token"

    org = "home"
    bucket = "energy"
    url = "http://localhost:8086"
    influxdb_service = InfluxDBService(org, bucket, url, token)

    collector = provide_smart_meter_collector(collector_name)

    try:
        measure = collector.collect()
        logging.debug(measure)
        influxdb_service.write_measure(measure)
    except Exception:
        logging.exception("collecting failure")


if __name__ == '__main__':
    argv = sys.argv[1:]
    # TODO: improve arg parsing
    debug_mode = argv[0].lower() == "true" if len(argv) >= 1 else False
    collector_name = argv[1].lower() if len(argv) >= 2 else "orno"

    if debug_mode:
        logging.basicConfig(level=logging.DEBUG)
    else:
        logging.basicConfig(level=logging.INFO)

    logging.info(f"Start monitoring, args: debug_mode={debug_mode}, collector_name={collector_name}")
    tl.start(block=True)
