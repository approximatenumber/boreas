import minimalmodbus

from lib.devices.device_configurations import ControllerConfig
from lib.devices.modbus_device import ModBusDevice


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

    def get_pv_voltage(self):
        return self.read_register(self.config.PV_VOLTAGE)

    def get_pv_current(self):
        return self.read_register(self.config.PV_CURRENT)

    def get_pv_power(self):
        return self.read_register(self.config.PV_POWER)

    def get_load_2_current(self):
        return self.read_register(self.config.LOAD_2_CURRENT)

    def get_load_1_current(self):
        return self.read_register(self.config.LOAD_1_CURRENT)

    def get_load_2_power(self):
        return self.read_register(self.config.LOAD_2_POWER)

    def get_load_1_power(self):
        return self.read_register(self.config.LOAD_1_POWER)

    def get_daily_wind_gen_energy(self):
        return self.read_register(self.config.DAILY_WIND_GEN_ENERGY)

    def get_accum_wind_gen_energy(self):
        high = self.read_register(self.config.ACCUM_WIND_GEN_ENERGY_HIGH)
        low = self.read_register(self.config.ACCUM_WIND_GEN_ENERGY_LOW)
        if not high or not low:
            return None
        return high+low

    def get_daily_solar_gen_energy(self):
        return self.read_register(self.config.DAILY_SOLAR_GEN_ENERGY)

    def get_accum_solar_gen_energy(self):
        high = self.read_register(self.config.ACCUM_SOLAR_GEN_ENERGY_HIGH)
        low = self.read_register(self.config.ACCUM_SOLAR_GEN_ENERGY_LOW)
        if not high or not low:
            return None
        return high+low

    def get_daily_gen_energy(self):
        return self.read_register(self.config.DAILY_GEN_ENERGY)

    def get_total_gen_energy(self):
        high = self.read_register(self.config.TOTAL_GEN_ENERGY_HIGH)
        low = self.read_register(self.config.TOTAL_GEN_ENERGY_LOW)
        if not high or not low:
            return None
        return high+low

    def get_daily_consump_energy(self):
        return self.read_register(self.config.DAILY_CONSUMP_ENERGY)

    def get_total_consump_energy(self):
        high = self.read_register(self.config.TOTAL_CONSUMP_ENERGY_HIGH)
        low = self.read_register(self.config.TOTAL_CONSUMP_ENERGY_LOW)
        if not high or not low:
            return None        
        return high+low
