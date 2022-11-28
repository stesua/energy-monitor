import logging

from collect import OrnaWe515Collector, FakeCollector
from influxdb import InfluxDBService
from timeloop import Timeloop
from datetime import timedelta

tl = Timeloop()


# TODO: configure interval
@tl.job(interval=timedelta(seconds=1))
def run_job():
    logging.basicConfig(level=logging.DEBUG)
    logging.info("Start monitoring")

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
    except Exception as e:
        logging.error(e)


if __name__ == '__main__':
    tl.start(block=True)
