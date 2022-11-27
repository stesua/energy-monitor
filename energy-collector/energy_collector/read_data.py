import minimalmodbus

if __name__ == '__main__':
    # TODO: select right port name
    instrument = minimalmodbus.Instrument('/dev/ttyUSB0', 1) # port name, slave address (in decimal)
    instrument.serial.baudrate = 9600
    # instrument.serial.bytesize = 8
    instrument.serial.parity   = minimalmodbus.serial.PARITY_EVEN # gituser-rk has changed it to PARITY_NONE don't know why
    # instrument.serial.stopbits = 1
    instrument.serial.timeout  = 0.10          # seconds
    # instrument.mode = minimalmodbus.MODE_RTU   # rtu or ascii mode
    # instrument.clear_buffers_before_each_transaction = True
    # instrument.debug = False
    #
    frequency = instrument.read_register(304, 2, 3, True)
    print(f'freq = {frequency} Hz')
    voltage = instrument.read_register(305, 2, 3, True)
    print(f"voltage = {voltage} V")
    current = instrument.read_long(313, 3, False, 0)
    print(f"current = {current} A")
    active_power = instrument.read_long(320, 3, False, 0)
    print(f"active_power = {active_power} kW")
    reactive_power =  instrument.read_long(328, 3, False, 0)
    print(f"reactive_power = {reactive_power} kvar")
    apparent_power = instrument.read_long(336, 3, False, 0)
    print(f"apparent_power = {apparent_power} kva")
    power_factory = instrument.read_register(344, 3, 3, True)
    print(f"power_factory = {power_factory}")

    # TODO: cannot found on doc
    # active_energy = self.smart_meter.instrument.read_registers(40960, 10, 3)
    # print(f"active_energy = {active_energy} ")
    # reactive_energy = self.smart_meter.instrument.read_registers(40990, 10, 3)
    # print(f"reactive_energy = {reactive_energy} ")

