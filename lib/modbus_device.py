import minimalmodbus


class ModBusDevice():
    def __init__(self, config=None):
        self.config = config
        self.conn = minimalmodbus.Instrument(
            self.config.PORT,
            self.config.SLAVE_ADDRESS,
            mode=self.config.MODBUS_MODE
        )
        self.conn.serial.baudrate = self.config.BAUDRATE
        self.conn.serial.timeout = self.config.READ_TIMEOUT

    def read_register(self, register: int) -> str:
        return self.conn.read_register(register, functioncode=3)