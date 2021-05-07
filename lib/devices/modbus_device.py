import minimalmodbus
from lib.logger import Logger


logger = Logger.get_logger('boreas')


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
        logger.debug(
            f"Reading from port={self.config.PORT}, slave={self.config.SLAVE_ADDRESS}, reg={register}")
        try:
            return self.conn.read_register(register, functioncode=3)
        except Exception as e:
            logger.error(f"Cannot read data due to error: {e}")
            return None
