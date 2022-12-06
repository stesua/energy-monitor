import dataclasses
import datetime
from unittest.mock import patch

from freezegun import freeze_time

from energy_collector.collect import RampPowerCollector, Measure, FixedCollector, RandomCollector, OrnaWe515Collector

dummy_date = datetime.datetime(2012, 1, 14)

dummy_measure = Measure(
    timestamp=dummy_date,
    frequency=50.0,
    voltage=230.0,
    current=1.0,
    active_power=0.0,
    reactive_power=100.0,
    apparent_power=240.0,
    power_factory=0.9
)

dummy_measure_ones = Measure(
    timestamp=dummy_date,
    frequency=1.0,
    voltage=1.0,
    current=1.0,
    active_power=1.0,
    reactive_power=1.0,
    apparent_power=1.0,
    power_factory=1.0
)


@freeze_time(dummy_date.strftime("%m/%d/%Y"))
@patch("minimalmodbus.Instrument")
def test_orna_we_515_collector(smart_meter_mock):
    smart_meter_mock.read_register.return_value = 1.0
    smart_meter_mock.read_long.return_value = 1
    sut = OrnaWe515Collector(smart_meter_mock)
    assert sut.collect() == dummy_measure_ones


@freeze_time(dummy_date.strftime("%m/%d/%Y"))
def test_random_collector():
    sut = RandomCollector()
    assert sut.collect() != sut.collect()


@freeze_time(dummy_date.strftime("%m/%d/%Y"))
@patch('random.uniform')
def test_random_collector_fixed_value(random_mock):
    random_mock.return_value = 1.0
    sut = RandomCollector()
    assert sut.collect() == Measure(
        timestamp=dummy_date,
        frequency=1.0,
        voltage=1.0,
        current=1.0,
        active_power=1.0,
        reactive_power=1.0,
        apparent_power=1.0,
        power_factory=1.0
    )


@freeze_time(dummy_date.strftime("%m/%d/%Y"))
def test_fixed_collector():
    sut = FixedCollector()
    assert sut.collect() == sut.collect()


@freeze_time(dummy_date.strftime("%m/%d/%Y"))
def test_ramp_power_collector():
    sut = RampPowerCollector()
    assert sut.collect() == dummy_measure
    assert sut.collect() == dataclasses.replace(dummy_measure, active_power=1.0)
    assert sut.collect() == dataclasses.replace(dummy_measure, active_power=2.0)
    assert sut.collect() != sut.collect()
