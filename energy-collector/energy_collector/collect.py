import minimalmodbus
from dataclasses import dataclass
from typing import Optional
from instrument import OrnaWe515

@dataclass
class Measure:
    """Energy meter measures"""
    frequency: float
    voltage: float
    current: float
    active_power: float
    reactive_power: float
    apparent_power: float
    power_factory: float
    active_energy: Optional[float] = None
    reactive_energy: Optional[float] = None

class MeasureException(Exception):
    """Raise for my specific kind of exception"""

class SmartMeterCollector:
    def __init__(self, smart_meter: OrnaWe515):
        self.smart_meter = smart_meter

    def collect(self) -> Measure:
        try:
            return Measure(
                # registeraddress, number_of_decimals=0, functioncode=3, signed=False
                frequency = self.smart_meter.instrument.read_register(304, 2, 3, True),
                voltage = self.smart_meter.instrument.read_register(305, 2, 3, True),
                #registeraddress, functioncode=3, signed=False, byteorder=0) in mA
                current = self.smart_meter.instrument.read_long(313, 3, False, 0),
                #registeraddress, functioncode=3, signed=False, byteorder=0)
                active_power = self.smart_meter.instrument.read_long(320, 3, False, 0),
                #registeraddress, functioncode=3, signed=False, byteorder=0)
                reactive_power =  self.smart_meter.instrument.read_long(328, 3, False, 0),
                #registeraddress, functioncode=3, signed=False, byteorder=0)
                apparent_power = self.smart_meter.instrument.read_long(336, 3, False, 0),
                power_factory = self.smart_meter.instrument.read_register(344, 3, 3, True),
                #read_registers(registeraddress, number_of_registers, functioncode=3) TODO: check transformation
                # active_energy = self.smart_meter.instrument.read_registers(40960, 10, 3),
                #read_registers(registeraddress, number_of_registers, functioncode=3) TODO: check transformation
                # reactive_energy = self.smart_meter.instrument.read_registers(40990, 10, 3)
            )
        except e:
            raise MeasureException("Fail to fetch measure") from e