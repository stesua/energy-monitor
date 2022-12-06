import logging
import random
from datetime import datetime
from dataclasses import dataclass
from minimalmodbus import Instrument
from typing import Optional

from energy_collector.instrument import OrnaWe515


@dataclass
class Measure:
    """Energy meter measures"""
    timestamp: datetime
    frequency: float
    voltage: float
    current: float
    active_power: float
    reactive_power: float
    apparent_power: float
    power_factory: float
    name: str = "energy"
    active_energy: Optional[float] = None
    reactive_energy: Optional[float] = None


class MeasureException(Exception):
    """Raise when error in the measure occur, typically due to hardware interface"""


class SmartMeterCollector:
    def collect(self) -> Measure:
        pass


class OrnaWe515Collector(SmartMeterCollector):
    def __init__(self, smart_meter_instrument: Instrument):
        self.smart_meter = smart_meter_instrument

    def collect(self) -> Measure:
        try:
            return Measure(
                timestamp=datetime.utcnow(),
                frequency=float(self.smart_meter.read_register(304, 2, 3, True)),
                voltage=float(self.smart_meter.read_register(305, 2, 3, True)),
                current=float(self.smart_meter.read_long(313, 3, False, 0)),
                active_power=float(self.smart_meter.read_long(320, 3, False, 0)),
                reactive_power=float(self.smart_meter.read_long(328, 3, False, 0)),
                apparent_power=float(self.smart_meter.read_long(336, 3, False, 0)),
                power_factory=float(self.smart_meter.read_register(344, 3, 3, True)),
                #read_registers(registeraddress, number_of_registers, functioncode=3) TODO: check transformation
                # active_energy=float(self.smart_meter.instrument.read_registers(40960, 10, 3)),
                #read_registers(registeraddress, number_of_registers, functioncode=3) TODO: check transformation
                # reactive_energy=float(self.smart_meter.instrument.read_registers(40990, 10, 3))
            )
        except Exception as e:
            raise MeasureException("Fail to fetch measure") from e


class RandomCollector(SmartMeterCollector):
    def collect(self) -> Measure:
        return Measure(
            timestamp=datetime.utcnow(),
            frequency=random.uniform(49.8, 50.2),
            voltage=random.uniform(228.0, 232.0),
            current=random.uniform(0.0, 15.0),
            active_power=random.uniform(0.0, 4000.0),
            reactive_power=random.uniform(0.0, 4000.0),
            apparent_power=random.uniform(0.0, 4000.0),
            power_factory=random.uniform(0.0, 2.0)
        )


class FixedCollector(SmartMeterCollector):
    def collect(self) -> Measure:
        return Measure(
            timestamp=datetime.utcnow(),
            frequency=50.0,
            voltage=230.0,
            current=1.0,
            active_power=230.0,
            reactive_power=100.0,
            apparent_power=240.0,
            power_factory=0.9
        )


class RampPowerCollector(SmartMeterCollector):
    power = -1.0

    def collect(self) -> Measure:
        self.power = self.power + 1.0
        return Measure(
            timestamp=datetime.utcnow(),
            frequency=50.0,
            voltage=230.0,
            current=1.0,
            active_power=self.power,
            reactive_power=100.0,
            apparent_power=240.0,
            power_factory=0.9
        )

# FIXME: orna collector must be lazy
# orna_collector_instance = OrnaWe515Collector()
fixed_collector_instance = FixedCollector()
random_collector_instance = RandomCollector()
# FIXME: ramp_power must be singleton or with shared state
ramp_power_collector_instance = RampPowerCollector()


def provide_smart_meter_collector(collector_name: str) -> SmartMeterCollector:
    if collector_name == "orna":
        return OrnaWe515Collector(OrnaWe515('/dev/ttyUSB0', 1))
        # return orna_collector_instance
    elif collector_name == "fixed":
        return fixed_collector_instance
    elif collector_name == "random":
        return random_collector_instance
    elif collector_name == "ramp-power":
        return ramp_power_collector_instance
    else:
        error_message = f"Cannot match any collector for {collector_name}"
        logging.error(error_message)
        raise ValueError(error_message)
