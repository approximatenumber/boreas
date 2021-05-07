from lib.devices.black_box_meter_device import BlackBoxMeterDevice
from lib.devices.device_configurations import SpeedMeterConfig


class TorqueMeter(BlackBoxMeterDevice):
    def __init__(self):
        super().__init__(config=SpeedMeterConfig)

    def get_speed(self):
        return self.write_value_and_read_answer(SpeedMeterConfig.SPEED_CMD)
