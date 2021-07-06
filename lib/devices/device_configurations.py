class ControllerConfig():
    SLAVE_ADDRESS = 41
    BAUDRATE = 9600
    PORT = '/dev/ttyRS485-1'
    MODBUS_MODE = 'rtu'
    READ_TIMEOUT = 1

    STATE_REG = 0
    BAT_VOLT_REG = 1
    WIND_VOLT_REG = 2
    WIND_CURR_REG = 3
    WIND_PWR_REG = 4
    WIND_ROT_SPEED_REG = 5
    PV_VOLTAGE = 6
    PV_CURRENT = 7
    PV_POWER = 8
    LOAD_2_CURRENT = 9
    LOAD_1_CURRENT = 10
    LOAD_2_POWER = 11
    LOAD_1_POWER = 12
    DAILY_WIND_GEN_ENERGY = 13
    ACCUM_WIND_GEN_ENERGY_HIGH = 14  # high
    ACCUM_WIND_GEN_ENERGY_LOW = 15  # low
    DAILY_SOLAR_GEN_ENERGY = 16
    ACCUM_SOLAR_GEN_ENERGY_HIGH = 17
    ACCUM_SOLAR_GEN_ENERGY_LOW = 18
    DAILY_GEN_ENERGY = 19
    TOTAL_GEN_ENERGY_HIGH = 20
    TOTAL_GEN_ENERGY_LOW = 21
    DAILY_CONSUMP_ENERGY = 22
    TOTAL_CONSUMP_ENERGY_HIGH = 23
    TOTAL_CONSUMP_ENERGY_LOW = 24


class WindSensorConfig():
    SLAVE_ADDRESS = 2
    BAUDRATE = 9600
    PORT = '/dev/ttyRS485-1'
    MODBUS_MODE = 'rtu'
    READ_TIMEOUT = 2

    WIND_REG = 42

class TorqueMeterConfig():
    PORT = '/dev/ttyRS485-2'
    BAUDRATE = 9600
    TIMEOUT = 1

    PEAK_CMD = '#01'

class SpeedMeterConfig():
    PORT = '/dev/ttyRS485-2'
    BAUDRATE = 9600
    TIMEOUT = 1

    SPEED_CMD = '#02'


class InverterConfig():
    PORT = '/dev/ttyMOD1'
    BAUDRATE = 19200
    TIMEOUT = 2

    _M_POWhourNET_L = [0x04, 0x4D]
    _M_POWhourNET_H = [0x04, 0x4E]
    _M_POWhourNET_HH = [0x04, 0x4F]