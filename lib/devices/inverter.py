import serial
import struct
import logging
from conf.device_configurations import InverterConfig
from lib.wrappers import retry

logger = logging.getLogger('boreas')

class Inverter():

    def __init__(self):
        self.config = InverterConfig()
        self.serial = serial.Serial(
            port=self.config.PORT,
            baudrate=self.config.BAUDRATE,
            timeout=self.config.TIMEOUT
        )

    def _send_packet_and_get_answer(self, packet):
        logger.info(f"Sending packet {packet}...")
        self.serial.flushInput()
        self.serial.flushOutput()
        for sent_byte in packet:
            self.serial.write(sent_byte)
            received_byte = self.serial.read(len(sent_byte))
            if sent_byte != received_byte:
                raise Exception(f"sent {sent_byte}, received {received_byte}")
        answer_packet = self.serial.readall()
        self._validate_answer_packet(answer_packet)
        logger.debug(f"Sent packet: {packet}, received packet: {answer_packet}")
        return answer_packet

    def _validate_answer_packet(self, packet):
        if not packet:
            raise Exception(f"Answer packet is empty")
        # first symbol indicates answer statys
        answer_type = chr(packet[0])
        if answer_type == 'o':  # otvet :)
            return packet
        elif answer_type == 'e':  # error
            raise Exception(f"Answer packet has error: {packet}")
        else:
            raise Exception(f"Unexpected packet: {packet}")

    @retry(retries=3, time_between_retries=2, exception_class=Exception)
    def _read_value_from_device(self, page_size, address, signed=False):
        packet = InverterPacket(page_size=page_size, address=address, packet_type='read').packet
        answer = self._send_packet_and_get_answer(packet)
        first_value_byte = 1
        last_value_byte = page_size + first_value_byte + 1  # 0x00 is for 1 byte; 0x03 is for 4 bytes
        value_in_bytes = answer[first_value_byte:last_value_byte]
        if type(value_in_bytes) == bytes:
            return int.from_bytes(value_in_bytes, 'little', signed=signed)
        elif type(value_in_bytes) == int:
            return value_in_bytes
        else:
            raise Exception(f"wrong value type {type(value_in_bytes)}: {value_in_bytes}")

    def get_pwr_consmp_from_net(self):
        """Power consumption from network."""
        _M_POWhourNET_L = self._read_value_from_device(page_size=0x00, address=self.config._M_POWhourNET_L)
        _M_POWhourNET_H = self._read_value_from_device(page_size=0x00, address=self.config._M_POWhourNET_H)
        _M_POWhourNET_HH = self._read_value_from_device(page_size=0x00, address=self.config._M_POWhourNET_HH)
        return (_M_POWhourNET_HH * 65536 + _M_POWhourNET_H * 256 + _M_POWhourNET_L) / 100

    def get_pwr_consmp_from_bat(self):
        """Power consumption from battery."""
        _M_POWhourMAP_L = self._read_value_from_device(page_size=0x00, address=self.config._M_POWhourMAP_L)
        _M_POWhourMAP_H = self._read_value_from_device(page_size=0x00, address=self.config._M_POWhourMAP_H)
        _M_POWhourMAP_HH = self._read_value_from_device(page_size=0x00, address=self.config._M_POWhourMAP_HH)
        return (_M_POWhourMAP_HH * 65536 + _M_POWhourMAP_H * 256 + _M_POWhourMAP_L) / 100

    def get_pwr_consmp_charge(self):
        def get_M_POWhourMAPCharge_L():
            return self._read_value_from_device(page_size=0x00, address=self.config._M_POWhourMAPCharge_L)
        def get_M_POWhourMAPCharge_H():
            return self._read_value_from_device(page_size=0x00, address=self.config._M_POWhourMAPCharge_H)
        def get_M_POWhourMAPCharge_HH():
            return self._read_value_from_device(page_size=0x00, address=self.config._M_POWhourMAPCharge_HH)
        _M_POWhourMAPCharge_L = get_M_POWhourMAPCharge_L()
        _M_POWhourMAPCharge_H = get_M_POWhourMAPCharge_H()
        _M_POWhourMAPCharge_HH = get_M_POWhourMAPCharge_HH()
        return (_M_POWhourMAPCharge_HH * 65536 + _M_POWhourMAPCharge_H * 256 + _M_POWhourMAPCharge_L) / 100

    def get_net_current_sign(self):
        _M_POWhourNET_sign_1 = self._read_value_from_device(page_size=0x00, address=self.config._M_POWhourNET_sign_1)
        _M_POWhourNET_sign_2 = self._read_value_from_device(page_size=0x00, address=self.config._M_POWhourNET_sign_2)
        _M_POWhourNET_sign_3 = self._read_value_from_device(page_size=0x00, address=self.config._M_POWhourNET_sign_3)
        _M_POWhourNET_sign_4 = self._read_value_from_device(page_size=0x00, address=self.config._M_POWhourNET_sign_4)
        return ((_M_POWhourNET_sign_4 << 24) + (_M_POWhourNET_sign_3 << 16) + (_M_POWhourNET_sign_2 << 8) + _M_POWhourNET_sign_1) / 100

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
        """"""
        _packet = [self.start_symbol, self.page_size, *self.address, self.checksum, self.END_SYMBOL]
        _bytes = []
        for element in _packet:
            # https://docs.python.org/3/library/struct.html#format-characters
            if element <= 255:
                size = 'B'  # unsigned char
            else:
                size = 'H'  # unsigned short
            _byte = struct.pack(size, element)
            _bytes.append(_byte)
        return _bytes

    @property
    def checksum(self):
        _sum = sum([self.READ_START_SYMBOL, self.page_size, *self.address])
        checksum = 0x100 - (_sum % 256)
        # check that checksum is correct
        assert sum([_sum, checksum]) % 256 == 0, f"Wrong checksum: {checksum}"
        return checksum


# inverer = Inverter()
# print(inverer.get_pwr_consmp_from_net())
