import logging

from datetime import datetime
from collect import SmartMeterCollector, Measure, MeasureException
from energy_collector.influxdb import InfluxDBService
from instrument import OrnaWe515
from timeloop import Timeloop
from datetime import timedelta

tl = Timeloop()
# TODO: configure
@tl.job(interval=timedelta(seconds=10))
def run_job():
    logging.basicConfig(level=logging.DEBUG)
    logging.info("Start monitoring")
    # TODO: change
    token = "zBrdmVUqqKmgSkjmJdVavMsdsJrAZv7znzR-s6sYPNidNwjsno8g-eQhropAJlbj2gq_1zyUpZxxN1vZH8YPgA=="
    org = "home"
    bucket = "energy"
    url = "http://192.168.1.248:8086"
    influxdb_service = InfluxDBService(org, bucket, url, token)
    collector = SmartMeterCollector(smart_meter=OrnaWe515())

    try:
        measure = collector.collect()
        fake_measure = Measure(
            timestamp=datetime.utcnow(),
            frequency=50,
            voltage=230,
            current=1,
            active_power=300,
            reactive_power=200,
            apparent_power=150,
            power_factory=1,
            active_energy=None,
            reactive_energy=None)
        logging.info(measure)
        influxdb_service.write_measure(measure)
    except MeasureException as e:
        logging.error(e)

if __name__ == '__main__':
    tl.start(block=True)
