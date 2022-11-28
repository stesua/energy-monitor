import logging
from influxdb_client import InfluxDBClient
from collect import SmartMeterCollector, Measure, MeasureException
from instrument import OrnaWe515

if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    logging.info("Start monitoring")
    # TODO: change
    token = "iGHIoYd-jIJ1piThJevsDcPmpSQzo3pV45GL0sSE0c34ESsP30ChBXSYQ0HP6IZhK6zgqI-cbuYLGWfWZ4iZNA=="
    org = "home"
    bucket = "energy"
    url = "http://localhost:8086"
    influxdb_client = InfluxDBClient(url=url, token=token, org=org)
    
    collector = SmartMeterCollector(smart_meter = OrnaWe515())

    try:
        measure = collector.collect()
        logging.info(measure)
    except MeasureException as e:
        logging.error(e)

