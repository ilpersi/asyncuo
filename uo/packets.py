import struct

import uo.serialize

from uo.packet_table import DYNAMIC_LENGTH


class UOPacket:
    def __init__(self, data: bytes, expected_packet_len: int):
        self.data = data
        self.expected_packet_len = expected_packet_len

        self._input = bytes()
        self._input += data

    def from_buffer(self):
        if self._input == bytes():
            return None

        cmd = self._input[0]
        expected_packet_len = self.expected_packet_len

        if expected_packet_len == DYNAMIC_LENGTH:
            if len(self._input) < 3:
                return None

            expected_packet_len = struct.unpack('>H', self._input[1:3])[0]
            if expected_packet_len < 3 or expected_packet_len > 0x8000:
                raise Exception("Malformed packet")

            if len(self._input) < expected_packet_len:
                return None

            data_start = 3
        else:
            if len(self._input) < expected_packet_len:
                return None

            data_start = 1

        data, self._input = self._input[data_start:expected_packet_len], self._input[expected_packet_len:]

        return uo.serialize.PacketReader(cmd, data)


class Relay:
    def __init__(self, packet):
        self.ip = packet.ipv4()
        self.port = packet.ushort()
        self.auth_id = packet.uint()


class Server:
    def __init__(self, packet):
        self.index = packet.ushort()
        self.name = packet.fixstring(32)
        self.percent_full = packet.byte()
        self.timezone = packet.byte()
        self.ip = packet.ipv4(True)


class ServerList:
    def __init__(self, packet):
        self.sys_info_flag = packet.byte()
        self.count = packet.ushort()
        self.servers = tuple(map(lambda x: Server(packet), range(self.count)))


class RazorFeatures:
    def __init__(self, packet):
        self.features = packet.byte()
