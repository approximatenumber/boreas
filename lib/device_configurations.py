class ControllerConfig():
    SLAVE_ADDRESS = 41
    BAUDRATE = 9600
    PORT = '/dev/ttyRS485-1'
    MODBUS_MODE = 'rtu'
    READ_TIMEOUT = 4

    STATE_REG = 0
    BAT_VOLT_REG = 1
    WIND_VOLT_REG = 2
    WIND_CURR_REG = 3
    WIND_PWR_REG = 4
    WIND_ROT_SPEED_REG = 5

class WindSensorConfig():
    SLAVE_ADDRESS = 2
    BAUDRATE = 9600
    PORT = '/dev/ttyRS485-1'
    MODBUS_MODE = 'rtu'
    READ_TIMEOUT = 4

    WIND_REG = 0x2A
