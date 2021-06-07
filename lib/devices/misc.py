class MiscDevices():

    CPU_TEMP_PATH = "/sys/class/thermal/thermal_zone0/temp"
    BOARD_TEPM_PATH = "/sys/class/hwmon/hwmon0/temp1_input"

    def __init__(self):
        pass

    def _get_value_from_fs(self, path: str, divide=1, _round=1) -> float:
        """Get value from local filesystem path.
        :param path: path to local file
        :param divide: division number
        :param _round: round number
        """
        try:
            raw_value = open(self.CPU_TEMP_PATH).read()
        except Exception:
            return None
        return round((int(raw_value) / divide), _round)

    def get_cpu_temp(self) -> int:
        """Get CPU temperature."""
        return self._get_value_from_fs(self.CPU_TEMP_PATH, divide=1000, _round=1)

    def get_board_temp(self) -> int:
        """Get board temperature."""
        return self._get_value_from_fs(self.BOARD_TEPM_PATH, divide=1000, _round=1)
