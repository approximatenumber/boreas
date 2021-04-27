from time import sleep
import logging
import argparse
from lib.mqtt_publisher import MQTTPublisher
from lib.controller import Controller
from lib.wind_sensor import WindSensor

PUBLISH_TIMEOUT = 5

publisher = MQTTPublisher()
controller = Controller()
wind_sensor = WindSensor()

data_dispath = {
    'controller': {
        'accum_solar_gen_energy': controller.get_accum_solar_gen_energy,
        'accum_wind_gen_energy': controller.get_accum_wind_gen_energy,
        'battery_voltage': controller.get_battery_voltage,
        'daily_consump_energy': controller.get_daily_consump_energy,
        'daily_gen_energy': controller.get_daily_gen_energy,
        'daily_solar_gen_energy': controller.get_daily_solar_gen_energy,
        'daily_wind_gen_energy': controller.get_daily_wind_gen_energy,
        'load_1_current': controller.get_load_1_current,
        'load_1_power': controller.get_load_1_power,
        'load_2_current': controller.get_load_2_current,
        'load_2_power': controller.get_load_2_power,
        'pv_current': controller.get_pv_current,
        'pv_power': controller.get_pv_power,
        'pv_voltage': controller.get_pv_voltage,
        'state': controller.get_state,
        'total_consump_energy': controller.get_total_consump_energy,
        'total_gen_energy': controller.get_total_gen_energy,
        'wind_current': controller.get_wind_current,
        'wind_power': controller.get_wind_power,
        'wind_rotation_speed': controller.get_wind_rotation_speed,
        'wind_voltage': controller.get_wind_voltage
    },
    'wind_sensor': {
        'wind_power': wind_sensor.get_wind_power
    }
}


def main():

    logger = logging.getLogger('boreas')
    parser = argparse.ArgumentParser()
    parser.add_argument('-d', '--debug', action='store_true', help='enable debug mode')
    args = parser.parse_args()

    if args.debug:
        logger.setLevel(logging.DEBUG)

    while True:
        for device, topic_to_function in data_dispath.items():
            for topic, function in topic_to_function.items():
                value = function()
                if not isinstance(value, (int, float)):
                    print(f"Cannot get data from device \"{device}\" for topic \"{topic}\"")
                    continue
                publisher.publish(topic=f"{device}/{topic}", value=value)
        sleep(PUBLISH_TIMEOUT)


if __name__ == '__main__':
    main()