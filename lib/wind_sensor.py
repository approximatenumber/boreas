import minimalmodbus

from lib.device_configurations import WindSensorConfig
from lib.modbus_device import ModBusDevice


class WindSensor(ModBusDevice):
    def __init__(self, config=WindSensorConfig):
        super().__init__(config=config)
    
    def get_wind_power(self):
        return self.read_register(self.config.WIND_REG)
