import minimalmodbus

from device import DeviceDefinition


class Controller(DeviceDefinition.Controller):

    def __init__(self):
        self.conn = minimalmodbus.Instrument(
            self.PORT,
            self.SLAVE_ADDRESS,
            mode=self.MODBUS_MODE
        )
        self.conn.serial.baudrate = self.BAUDRATE
        self.conn.serial.timeout = self.READ_TIMEOUT

    def _get_data(self, register: int, decimals: int = 1) -> float:
        return self.conn.read_register(register, decimals, functioncode=3)

    def get_state(self):
        return self._get_data(self.STATE_REG, self.STATE_DECIM)

    def get_battery_voltage(self):
        return self._get_data(self.BAT_VOLT_REG)

    def get_wind_voltage(self):
        return self._get_data(self.WIND_VOLT_REG)

    def get_wind_current(self):
        return self._get_data(self.WIND_CURR_REG)

    def get_wind_power(self):
        return self._get_data(self.WIND_PWR_REG)

    def get_wind_rotation_speed(self):
        return self._get_data(self.WIND_ROT_SPEED_REG)


controller = Controller()
print(controller.get_state())
