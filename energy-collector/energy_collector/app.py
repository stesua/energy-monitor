import datetime
import logging

from collect import OrnaWe515Collector, FakeCollector
from influxdb import InfluxDBService
from timeloop import Timeloop
from datetime import timedelta, datetime

tl = Timeloop()
logging.basicConfig(level=logging.DEBUG)


# TODO: configure interval
@tl.job(interval=timedelta(seconds=1))
def run_job():
    logging.debug(f"monitoring job triggered at {datetime.utcnow()}")
    # TODO: change
    # raspberry
    token = "zBrdmVUqqKmgSkjmJdVavMsdsJrAZv7znzR-s6sYPNidNwjsno8g-eQhropAJlbj2gq_1zyUpZxxN1vZH8YPgA=="
    # mac
    # token = "OZxcsRhjMmh0TpJZxrcya_wZJFJPwQ_QExVbreH2XqC7wans6G_Fs87-Uu7UhvG-TwsxJHa4g9U-4hRBH3h3TQ=="

    org = "home"
    bucket = "energy"
    url = "http://localhost:8086"
    influxdb_service = InfluxDBService(org, bucket, url, token)

    # TODO: use factory instead
    collector = OrnaWe515Collector()
    # collector = FakeCollector()

    try:
        measure = collector.collect()
        logging.info(measure)
        influxdb_service.write_measure(measure)
    except Exception:
        logging.exception("collecting failure")


if __name__ == '__main__':
    logging.info("Start monitoring")
    tl.start(block=True)
