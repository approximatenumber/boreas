import serial
import time
import re
import logging

logger = logging.getLogger('boreas')

from lib.wrappers import retry

class BlackBoxMeterDevice():
    def __init__(self, config=None):
        self.conn = serial.Serial(
            config.PORT,
            config.BAUDRATE,
            timeout=config.TIMEOUT)

    def _write_value(self, value):
        """Write value to port and sleep a little bit."""
        self.conn.write(f"{value}\r".encode())
        time.sleep(0.25)

    def _read_value(self):
        """Read raw value from port, clean it up and convert to float."""
        raw_value = self.conn.read_all().decode()
        # remove extra symbols from raw string
        return re.sub(r'[=@\r]','', raw_value)
    
    @retry(retries=3, time_between_retries=0.1, exception_class=Exception)
    def __write_value_and_read_answer(self, value):
        self._write_value(value)
        value = self._read_value()
        return float(value) if value else None

    def write_value_and_read_answer(self, value):
        try:
            return self.__write_value_and_read_answer(value)
        except Exception as err:
            logger.error(f"Cannot write value {value} and read an answer: {err}")
            return None
