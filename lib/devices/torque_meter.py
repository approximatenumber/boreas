from lib.devices.device_configurations import TorqueMeterConfig
from lib.devices.black_box_meter_device import BlackBoxMeterDevice
from lib.decorators import multiply_by_10

class TorqueMeter(BlackBoxMeterDevice):
    def __init__(self):
        super().__init__(config=TorqueMeterConfig)

    @multiply_by_10
    def get_peak(self):
        return self.write_value_and_read_answer(TorqueMeterConfig.PEAK_CMD)
