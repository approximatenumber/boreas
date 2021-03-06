#!/usr/bin/env python3

from time import sleep
import logging
import argparse
from typing import Dict, List
import threading

from lib.mqtt_publisher import MQTTPublisher
from lib.devices.controller import Controller
from lib.devices.wind_sensor import WindSensor
from lib.devices.torque_meter import TorqueMeter
from lib.devices.speed_meter import SpeedMeter
from lib.devices.inverter import Inverter
from lib.devices.misc import MiscDevices
from lib.logger import Logger


PUBLISH_TIMEOUT = 5
ENABLED_DEVICES = ['controller', 'wind_sensor', 'speed_meter', 'torque_meter', 'misc']


logger = Logger.get_logger('boreas')


publisher = MQTTPublisher()
controller = Controller()
wind_sensor = WindSensor()
torque_meter = TorqueMeter()
speed_meter = SpeedMeter()
inverter = Inverter()
misc_devices = MiscDevices()

dispath = {
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
    },
    'speed_meter': { 
        'speed': speed_meter.get_speed
    },
    'torque_meter': {
        'torque': torque_meter.get_peak
    },
    'inverter': {
        'pwr_consmp_from_net': inverter.get_pwr_consmp_from_net,
        'pwr_consmp_from_bat': inverter.get_pwr_consmp_from_bat,
        'pwr_consmp_charge': inverter.get_pwr_consmp_charge,
        'net_current_sign': inverter.get_net_current_sign
    },
    'misc': {
        'cpu_temp': misc_devices.get_cpu_temp,
        'board_temp': misc_devices.get_board_temp
    }
}


def _publish_topics(device2topics: Dict[str, str]):
    for device, topic2value in device2topics.items():
        if not topic2value:
            logger.warning(f"No data to publish for device {device}")
            continue
        for topic, value in topic2value.items():
            publisher.publish(topic=f"{device}/{topic}", value=value)
            logger.info(f"===> Published: topic={device}/{topic}, value={value}")


def collect_data_and_publish(devices: List[str]):
    while True:
        device2topics = {}
        for device in devices:
            device2topics[device] = {}
            logger.info(f"=> Reading device {device}")
            for topic, function in dispath[device].items():
                value = function()
                if not isinstance(value, (int, float)):
                    logger.error(f"===> Cannot get data from device \"{device}\" for topic \"{topic}\"")
                    # logger.error(f"Skipping further readings from \"{device}\" until next try")
                    continue
                device2topics[device][topic] = value

        _publish_topics(device2topics)
        sleep(PUBLISH_TIMEOUT)


def main():
    
    parser = argparse.ArgumentParser()
    parser.add_argument('-d', '--debug', action='store_true', help='enable debug mode')
    parser.add_argument('-o', '--only-device', required=False, action='store', help='poll only one device')
    args = parser.parse_args()

    if args.debug:
        logger.setLevel(logging.DEBUG)


    # first serial port
    devices_on_same_port1 = ['controller', 'wind_sensor']
    # second serial port
    devices_on_same_port2 = ['torque_meter', 'speed_meter']
    # third serial port
    devices_on_same_port3 = ['inverter']
    # misc devices
    misc_devices = ['misc']

    if args.only_device:
        devices_to_scan = [[args.only_device]]
    else:
        devices_to_scan = [devices_on_same_port1, devices_on_same_port2, devices_on_same_port3, misc_devices]

    threads = []
    for devices_per_port in devices_to_scan:
        thread = threading.Thread(target=collect_data_and_publish, args=([devices_per_port]))
        thread.start()
        threads.append(thread)

    for thread in threads:
        thread.join()


if __name__ == '__main__':
    main()
