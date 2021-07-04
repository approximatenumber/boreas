import serial
import struct
from typing import ByteString
from lib.devices.device_configurations import InverterConfig


class Inverter():

    def __init__(self):
        self.config = InverterConfig()
        self.device = serial.Serial(
            port=self.config.PORT,
            baudrate=self.config.BAUDRATE,
            timeout=self.config.TIMEOUT
        )

    def _send_packet_and_get_answer(self, packet):
        for sent_byte in packet:
            self.serial.write(sent_byte)
            received_byte = self.read(1)
            if sent_byte != received_byte:
                raise Exception(f"sent {sent_byte}, received {received_byte}")
        answer = self.readall()
        return answer

    def get_pwr_consmp_from_net(self):
        """Power consumption from network."""
        packet = InverterPacket(
            page_size=0x00, 
            address=self.config.PWR_CONSMP_FROM_NET, 
            packet_type='read').packet
        return self._send_packet_and_get_answer(packet)


class InverterPacket():

    READ_START_SYMBOL = 0x72
    END_SYMBOL = 0x0A

    def __init__(self, page_size, address, packet_type='read'):
        self.page_size = page_size
        self.address = address
        self.packet_type = packet_type

    @property
    def start_symbol(self):
        return self.READ_START_SYMBOL if self.packet_type == 'read' else None

    @property
    def packet(self):
        _packet = [self.start_symbol, self.page_size, *self.address, self.checksum, self.END_SYMBOL]
        return [struct.pack('B', _byte) for _byte in _packet]

    @property
    def checksum(self):
        checksum = 0x100 - (sum([self.READ_START_SYMBOL, self.page_size, *self.address]) % 256)
        return checksum
