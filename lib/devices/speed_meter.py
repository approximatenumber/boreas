from lib.devices.black_box_meter_device import BlackBoxMeterDevice
from lib.devices.device_configurations import SpeedMeterConfig
from lib.decorators import multiply_by_10


class SpeedMeter(BlackBoxMeterDevice):
    def __init__(self):
        super().__init__(config=SpeedMeterConfig)

    @multiply_by_10
    def get_speed(self):
        return self.write_value_and_read_answer(SpeedMeterConfig.SPEED_CMD)
