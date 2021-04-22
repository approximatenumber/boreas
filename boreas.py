from lib.mqtt_publisher import MQTTPublisher
from lib.devices import Controller, WindSensor

publisher = MQTTPublisher()
controller = Controller()
wind_sensor = WindSensor()

data_dispath = {
    'controller': {
        'bat_voltage': controller.get_battery_voltage,
    },
    'wind_sensor': {
        'wind_power': wind_sensor.get_wind_power
    }
}

for device, topic_to_function in data_dispath.items():
    for topic, function in topic_to_function.items():
        value = function()
        if not value:
            print(f"Cannot get data from \"{device}\" for topic \"{topic}\"")
            continue
        publisher.publish(topic=f"{device}/{topic}", value=value)
