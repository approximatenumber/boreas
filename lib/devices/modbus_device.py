import minimalmodbus
from lib.logger import Logger
from lib.wrappers import retry


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
        try:
            self.__read_register(register)
        except Exception as e:
            logger.error(f"Cannot read data due to error: {e}")
            return None

    @retry(retries=5, time_between_retries=0.2, exception_class=Exception)
    def __read_register(self, register: int) -> str:
        logger.debug(
            f"Reading from port={self.config.PORT}, slave={self.config.SLAVE_ADDRESS}, reg={register}")
        return self.conn.read_register(register, functioncode=3)
