import struct

from uo.packet_table import DYNAMIC_LENGTH


def decode_uchar(value):
    if value < 0x100:
        return chr(value)
    else:
        return '?'


def decode_ustring(x):
    result = u''
    i = 0
    while i < len(x):
        result += decode_uchar(struct.unpack('>H', x[i:i+2])[0])
        i += 2
    return result


def decode_ustring_list(x):
    result = []
    i = 0
    while i < len(x):
        p_len = struct.unpack('>H', x[i:i+2])[0]
        i += 2
        result.append(decode_ustring(x[i:i+p_len*2]))
        i += p_len * 2

    return result


class PacketReader:
    def __init__(self, cmd: int, data: bytes):
        self.cmd = cmd
        self._data = data

    def __len__(self):
        return len(self._data)

    def __repr__(self):
        return "PacketReader for cmd {} {} bytes".format(hex(self.cmd).upper(), len(self)+1)

    @property
    def raw_data(self):
        return self._data

    def data(self, length):
        if len(self._data) < length:
            raise Exception("Packet {} is too short".format(self.cmd))
        x, self._data = self._data[:length], self._data[length:]
        return x

    def ulong(self):
        return struct.unpack('>Q', self.data(8))[0]

    def uint(self):
        return struct.unpack('>I', self.data(4))[0]

    def ushort(self):
        return struct.unpack('>H', self.data(2))[0]

    def byte(self):
        return struct.unpack('>B', self.data(1))[0]

    def boolean(self):
        return self.byte() != 0

    def fixstring(self, length):
        return self.data(length).replace(b'\x00', b'')

    def cstring(self):
        i = self._data.index(b'\x00')
        x, self._data = self._data[:i], self._data[i+1:]
        return x

    def pstring(self):
        return self.fixstring(self.byte())

    def ucstring(self):
        x = ''
        while True:
            i = self.ushort()
            if i == 0:
                break
            x += decode_uchar(i)
        return x

    def ipv4(self, to_reverse=False):
        ipv4_raw = reversed(struct.unpack('4B', self.data(4))) if to_reverse else struct.unpack('4B', self.data(4))
        return '.'.join(map(str, ipv4_raw))


class PacketWriter:
    def __init__(self, cmd: int, length: int):
        self._data: bytes = bytes()
        self.byte(cmd)
        self._length = length

    def data(self, x):
        self._data += x

    def uint(self, x):
        self.data(struct.pack('>I', x))

    def ushort(self, x: int):
        assert 0 <= x < 65536
        self.data(struct.pack('>H', x))

    def sshort(self, x):
        assert -32768 <= x < 32768
        self.data(struct.pack('>h', x))

    def byte(self, x):
        assert 0 <= x < 256
        self.data(struct.pack('>B', x))

    def sbyte(self, x):
        assert -128 <= x < 128
        self.data(struct.pack('>b', x))

    def boolean(self, x):
        if x:
            self.byte(1)
        else:
            self.byte(0)

    def fixstring(self, x: bytes, length: int):
        if len(x) > length:
            raise Exception("String is too long")
        self.data(x)
        self.data(b'\x00' * (length - len(x)))

    def cstring(self, x):
        self.data(x)
        self.byte(0)

    def ucstring(self, x):
        for ch in x:
            self.ushort(ord(ch))
        self.ushort(0)

    def ipv4(self, x: str, to_reverse: bool=False):
        raw_ip = reversed(x.split('.')) if to_reverse else x.split('.')

        for ip_part in raw_ip:
            self.byte(int(ip_part))

    def finish(self):
        data: bytes = self._data
        if self._length == DYNAMIC_LENGTH:
            if len(data) > 0xf000:
                raise Exception("Packet too large")
            data = bytes([self._data[0]]) + bytes(struct.pack('>H', len(self._data) + 2)) + bytes(self._data[1:])
        else:
            if len(data) != self._length:
                print(self._length, repr(data))
                raise Exception("Invalid packet length")
        return data
