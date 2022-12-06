import minimalmodbus


class OrnaWe515(minimalmodbus.Instrument):

    def __init__(self, port: str, slaveaddress: int):
        super().__init__(port, slaveaddress)
        self.serial.baudrate = 9600
        self.serial.parity = minimalmodbus.serial.PARITY_EVEN
        # TODO try to increase timeout to avoid: minimalmodbus.NoResponseError: No communication with the instrument (no answer)
        self.serial.timeout = 0.10          # seconds
        self.debug = False

    
