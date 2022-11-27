import minimalmodbus


class OrnaWe515:

    def __init__(self):
        self.instrument = minimalmodbus.Instrument('/dev/ttyUSB0', 1)
        self.instrument.serial.baudrate = 9600
        self.instrument.serial.parity   = serial.PARITY_EVEN
        self.instrument.serial.timeout  = 0.10          # seconds
        self.instrument.debug = False

    
