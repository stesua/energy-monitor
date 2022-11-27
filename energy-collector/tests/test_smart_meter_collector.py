from energy_collector import __version__
import dummy_serial
import test_minimalmodbus
# dummy_serial.RESPONSES = test_minimalmodbus.RESPONSES  # Load previously recorded responses
import minimalmodbus

def test_read_frequency():
    sut = SmartMeterCollector(dummy_serial.Serial)
    assert __version__ == '0.1.0'
