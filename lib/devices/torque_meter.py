from conf.device_configurations import TorqueMeterConfig
from lib.devices.black_box_meter_device import BlackBoxMeterDevice

class TorqueMeter(BlackBoxMeterDevice):
    def __init__(self):
        super().__init__(config=TorqueMeterConfig)

    def get_peak(self):
        return self.write_value_and_read_answer(TorqueMeterConfig.PEAK_CMD)
