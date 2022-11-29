import random
from datetime import datetime
from dataclasses import dataclass
from typing import Optional
from instrument import OrnaWe515


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
    """Raise for my specific kind of exception"""


class SmartMeterCollector:
    def collect(self) -> Measure:
        pass


class OrnaWe515Collector(SmartMeterCollector):
    def __init__(self):
        self.smart_meter = OrnaWe515()

    def collect(self) -> Measure:
        try:
            return Measure(
                timestamp=datetime.utcnow(),
                frequency=float(self.smart_meter.instrument.read_register(304, 2, 3, True)),
                voltage=float(self.smart_meter.instrument.read_register(305, 2, 3, True)),
                current=float(self.smart_meter.instrument.read_long(313, 3, False, 0)),
                active_power=float(self.smart_meter.instrument.read_long(320, 3, False, 0)),
                reactive_power=float(self.smart_meter.instrument.read_long(328, 3, False, 0)),
                apparent_power=float(self.smart_meter.instrument.read_long(336, 3, False, 0)),
                power_factory=float(self.smart_meter.instrument.read_register(344, 3, 3, True)),
                #read_registers(registeraddress, number_of_registers, functioncode=3) TODO: check transformation
                # active_energy=float(self.smart_meter.instrument.read_registers(40960, 10, 3)),
                #read_registers(registeraddress, number_of_registers, functioncode=3) TODO: check transformation
                # reactive_energy=float(self.smart_meter.instrument.read_registers(40990, 10, 3))
            )
        except Exception as e:
            raise MeasureException("Fail to fetch measure") from e


class FakeCollector(SmartMeterCollector):
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
