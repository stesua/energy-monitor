import logging
from influxdb import InfluxDBClient
from collect import SmartMeterCollector
from instrument import OrnaWe515

if __name__ == '__main__':

    # client = InfluxDBClient(influx_config['host'],
    #                         influx_config['port'],
    #                         influx_config['user'],
    #                         influx_config['password'],
    #                         influx_config['dbname'])

    collector = SmartMeterCollector(smart_meter = OrnaWe515())

    try:
        measure = collector.collect()
        logging.debug(measure)
    except MeasureException as e:
        logging.error(e)

