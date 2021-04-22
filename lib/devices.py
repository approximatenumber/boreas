import minimalmodbus

from lib.device_configurations import ControllerConfig, WindSensorConfig


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


class Controller(ModBusDevice):

    def __init__(self, config=ControllerConfig):
        super().__init__(config=config)

    def get_state(self):
        return self.read_register(self.config.STATE_REG)

    def get_battery_voltage(self):
        return self.read_register(self.config.BAT_VOLT_REG)

    def get_wind_voltage(self):
        return self.read_register(self.config.WIND_VOLT_REG)

    def get_wind_current(self):
        return self.read_register(self.config.WIND_CURR_REG)

    def get_wind_power(self):
        return self.read_register(self.config.WIND_PWR_REG)

    def get_wind_rotation_speed(self):
        return self.read_register(self.config.WIND_ROT_SPEED_REG)


class WindSensor(ModBusDevice):
    def __init__(self, config=WindSensorConfig):
        super().__init__(config=config)
    
    def get_wind_power(self):
        return self.read_register(self.config.WIND_REG)
