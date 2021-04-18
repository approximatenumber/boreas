from mqtt_pulisher import MQTTPublisher
from controller import Controller

publisher = MQTTPublisher()
controller = Controller()


bat_voltage = controller.get_battery_voltage()
publisher.publish('bat_voltage', bat_voltage)
