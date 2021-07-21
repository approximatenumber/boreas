from conf.device_configurations import WindSensorConfig
from lib.devices.modbus_device import ModBusDevice
from lib.wrappers import divide_by_100


class WindSensor(ModBusDevice):
    def __init__(self, config=WindSensorConfig):
        super().__init__(config=config)

    @divide_by_100
    def get_wind_power(self):
        return self.read_register(self.config.WIND_REG)
