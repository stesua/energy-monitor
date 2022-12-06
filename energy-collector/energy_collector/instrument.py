import minimalmodbus


class OrnaWe515(minimalmodbus.Instrument):

    def __init__(self, port: str, slaveaddress: int):
        super().__init__(port, slaveaddress)
        self.serial.baudrate = 9600
        self.serial.parity = minimalmodbus.serial.PARITY_EVEN
        self.serial.timeout = 0.4
        self.debug = False

    
