class MiscDevices():

    CPU_TEMP_PATH = "/sys/class/thermal/thermal_zone0/temp"

    def __init__(self):
        pass

    def get_cpu_temp(self) -> int:
        """Get CPU temperature."""
        raw_temp = open(self.CPU_TEMP_PATH).read()
        return round(int(raw_temp) / 1000)
