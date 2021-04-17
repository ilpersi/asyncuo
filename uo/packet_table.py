from uo.client_version import Version

DYNAMIC_LENGTH = -1


class PacketTable:
    def __init__(self, version: Version):
        self.version: Version = version

        # courtesy of https://github.com/markdwags/Razor/blob/master/Razor/Network/PacketTable.cs
        self._packet_table: list[int] = [
            0x0068,  # 0x00
            0x0005,  # 0x01
            0x0007,  # 0x02
            DYNAMIC_LENGTH,  # 0x03
            0x0002,  # 0x04
            0x0005,  # 0x05
            0x0005,  # 0x06
            0x0007,  # 0x07
            0x000E,  # 0x08
            0x0005,  # 0x09
            0x000B,  # 0x0A
            0x010A,  # 0x0B
            DYNAMIC_LENGTH,  # 0x0C
            0x0003,  # 0x0D
            DYNAMIC_LENGTH,  # 0x0E
            0x003D,  # 0x0F
            0x00D7,  # 0x10
            DYNAMIC_LENGTH,  # 0x11
            DYNAMIC_LENGTH,  # 0x12
            0x000A,  # 0x13
            0x0006,  # 0x14
            0x0009,  # 0x15
            0x0001,  # 0x16
            DYNAMIC_LENGTH,  # 0x17
            DYNAMIC_LENGTH,  # 0x18
            DYNAMIC_LENGTH,  # 0x19
            DYNAMIC_LENGTH,  # 0x1A
            0x0025,  # 0x1B
            DYNAMIC_LENGTH,  # 0x1C
            0x0005,  # 0x1D
            0x0004,  # 0x1E
            0x0008,  # 0x1F
            0x0013,  # 0x20
            0x0008,  # 0x21
            0x0003,  # 0x22
            0x001A,  # 0x23
            0x0007,  # 0x24
            0x0014,  # 0x25
            0x0005,  # 0x26
            0x0002,  # 0x27
            0x0005,  # 0x28
            0x0001,  # 0x29
            0x0005,  # 0x2A
            0x0002,  # 0x2B
            0x0002,  # 0x2C
            0x0011,  # 0x2D
            0x000F,  # 0x2E
            0x000A,  # 0x2F
            0x0005,  # 0x30
            0x0001,  # 0x31
            0x0002,  # 0x32
            0x0002,  # 0x33
            0x000A,  # 0x34
            0x028D,  # 0x35
            DYNAMIC_LENGTH,  # 0x36
            0x0008,  # 0x37
            0x0007,  # 0x38
            0x0009,  # 0x39
            DYNAMIC_LENGTH,  # 0x3A
            DYNAMIC_LENGTH,  # 0x3B
            DYNAMIC_LENGTH,  # 0x3C
            0x0002,  # 0x3D
            0x0025,  # 0x3E
            DYNAMIC_LENGTH,  # 0x3F
            0x00C9,  # 0x40
            DYNAMIC_LENGTH,  # 0x41
            DYNAMIC_LENGTH,  # 0x42
            0x0229,  # 0x43
            0x02C9,  # 0x44
            0x0005,  # 0x45
            DYNAMIC_LENGTH,  # 0x46
            0x000B,  # 0x47
            0x0049,  # 0x48
            0x005D,  # 0x49
            0x0005,  # 0x4A
            0x0009,  # 0x4B
            DYNAMIC_LENGTH,  # 0x4C
            DYNAMIC_LENGTH,  # 0x4D
            0x0006,  # 0x4E
            0x0002,  # 0x4F
            DYNAMIC_LENGTH,  # 0x50
            DYNAMIC_LENGTH,  # 0x51
            DYNAMIC_LENGTH,  # 0x52
            0x0002,  # 0x53
            0x000C,  # 0x54
            0x0001,  # 0x55
            0x000B,  # 0x56
            0x006E,  # 0x57
            0x006A,  # 0x58
            DYNAMIC_LENGTH,  # 0x59
            DYNAMIC_LENGTH,  # 0x5A
            0x0004,  # 0x5B
            0x0002,  # 0x5C
            0x0049,  # 0x5D
            DYNAMIC_LENGTH,  # 0x5E
            0x0031,  # 0x5F
            0x0005,  # 0x60
            0x0009,  # 0x61
            0x000F,  # 0x62
            0x000D,  # 0x63
            0x0001,  # 0x64
            0x0004,  # 0x65
            DYNAMIC_LENGTH,  # 0x66
            0x0015,  # 0x67
            DYNAMIC_LENGTH,  # 0x68
            DYNAMIC_LENGTH,  # 0x69
            0x0003,  # 0x6A
            0x0009,  # 0x6B
            0x0013,  # 0x6C
            0x0003,  # 0x6D
            0x000E,  # 0x6E
            DYNAMIC_LENGTH,  # 0x6F
            0x001C,  # 0x70
            DYNAMIC_LENGTH,  # 0x71
            0x0005,  # 0x72
            0x0002,  # 0x73
            DYNAMIC_LENGTH,  # 0x74
            0x0023,  # 0x75
            0x0010,  # 0x76
            0x0011,  # 0x77
            DYNAMIC_LENGTH,  # 0x78
            0x0009,  # 0x79
            DYNAMIC_LENGTH,  # 0x7A
            0x0002,  # 0x7B
            DYNAMIC_LENGTH,  # 0x7C
            0x000D,  # 0x7D
            0x0002,  # 0x7E
            DYNAMIC_LENGTH,  # 0x7F
            0x003E,  # 0x80
            DYNAMIC_LENGTH,  # 0x81
            0x0002,  # 0x82
            0x0027,  # 0x83
            0x0045,  # 0x84
            0x0002,  # 0x85
            DYNAMIC_LENGTH,  # 0x86
            DYNAMIC_LENGTH,  # 0x87
            0x0042,  # 0x88
            DYNAMIC_LENGTH,  # 0x89
            DYNAMIC_LENGTH,  # 0x8A
            DYNAMIC_LENGTH,  # 0x8B
            0x000B,  # 0x8C
            DYNAMIC_LENGTH,  # 0x8D
            DYNAMIC_LENGTH,  # 0x8E
            DYNAMIC_LENGTH,  # 0x8F
            0x0013,  # 0x90
            0x0041,  # 0x91
            DYNAMIC_LENGTH,  # 0x92
            0x0063,  # 0x93
            DYNAMIC_LENGTH,  # 0x94
            0x0009,  # 0x95
            DYNAMIC_LENGTH,  # 0x96
            0x0002,  # 0x97
            DYNAMIC_LENGTH,  # 0x98
            0x001A,  # 0x99
            DYNAMIC_LENGTH,  # 0x9A
            0x0102,  # 0x9B
            0x0135,  # 0x9C
            0x0033,  # 0x9D
            DYNAMIC_LENGTH,  # 0x9E
            DYNAMIC_LENGTH,  # 0x9F
            0x0003,  # 0xA0
            0x0009,  # 0xA1
            0x0009,  # 0xA2
            0x0009,  # 0xA3
            0x0095,  # 0xA4
            DYNAMIC_LENGTH,  # 0xA5
            DYNAMIC_LENGTH,  # 0xA6
            0x0004,  # 0xA7
            DYNAMIC_LENGTH,  # 0xA8
            DYNAMIC_LENGTH,  # 0xA9
            0x0005,  # 0xAA
            DYNAMIC_LENGTH,  # 0xAB
            DYNAMIC_LENGTH,  # 0xAC
            DYNAMIC_LENGTH,  # 0xAD
            DYNAMIC_LENGTH,  # 0xAE
            0x000D,  # 0xAF
            DYNAMIC_LENGTH,  # 0xB0
            DYNAMIC_LENGTH,  # 0xB1
            DYNAMIC_LENGTH,  # 0xB2
            DYNAMIC_LENGTH,  # 0xB3
            DYNAMIC_LENGTH,  # 0xB4
            0x0040,  # 0xB5
            0x0009,  # 0xB6
            DYNAMIC_LENGTH,  # 0xB7
            DYNAMIC_LENGTH,  # 0xB8
            0x0003,  # 0xB9 #aggiornato da 3 a 5
            0x0006,  # 0xBA
            0x0009,  # 0xBB
            0x0003,  # 0xBC
            DYNAMIC_LENGTH,  # 0xBD
            DYNAMIC_LENGTH,  # 0xBE
            DYNAMIC_LENGTH,  # 0xBF
            0x0024,  # 0xC0
            DYNAMIC_LENGTH,  # 0xC1
            DYNAMIC_LENGTH,  # 0xC2
            DYNAMIC_LENGTH,  # 0xC3
            0x0006,  # 0xC4
            0x00CB,  # 0xC5
            0x0001,  # 0xC6
            0x0031,  # 0xC7
            0x0002,  # 0xC8
            0x0006,  # 0xC9
            0x0006,  # 0xCA
            0x0007,  # 0xCB
            DYNAMIC_LENGTH,  # 0xCC
            0x0001,  # 0xCD
            DYNAMIC_LENGTH,  # 0xCE
            0x004E,  # 0xCF
            DYNAMIC_LENGTH,  # 0xD0
            0x0002,  # 0xD1
            0x0019,  # 0xD2
            DYNAMIC_LENGTH,  # 0xD3
            DYNAMIC_LENGTH,  # 0xD4
            DYNAMIC_LENGTH,  # 0xD5
            DYNAMIC_LENGTH,  # 0xD6
            DYNAMIC_LENGTH,  # 0xD7
            DYNAMIC_LENGTH,  # 0xD8
            0x010C,  # 0xD9
            DYNAMIC_LENGTH,  # 0xDA
            DYNAMIC_LENGTH,  # 0xDB
            0x09,  # dc
            DYNAMIC_LENGTH,  # dd
            DYNAMIC_LENGTH,  # de
            DYNAMIC_LENGTH,  # df
            DYNAMIC_LENGTH,  # e0
            DYNAMIC_LENGTH,  # e1
            0x0A,  # e2
            DYNAMIC_LENGTH,  # e3
            DYNAMIC_LENGTH,  # e4
            DYNAMIC_LENGTH,  # e5
            0x05,  # e6
            0x0C,  # e7
            0x0D,  # e8
            0x4B,  # e9
            0x03,  # ea
            DYNAMIC_LENGTH,  # eb
            DYNAMIC_LENGTH,  # ec
            DYNAMIC_LENGTH,  # ed
            0x0A,  # ee
            0x0015,  # ef -> mortacci tua
            DYNAMIC_LENGTH,  # f0
            0x09,  # f1
            0x19,  # f2
            0x1A,  # f3 -> altro mortacci tua
            DYNAMIC_LENGTH,  # f4
            0x15,  # f5
            DYNAMIC_LENGTH,  # f6
            DYNAMIC_LENGTH,  # f7
            0x6A,  # f8
            DYNAMIC_LENGTH,  # f9
            0x01,  # fa
            0x02,  # fb
            DYNAMIC_LENGTH,  # fc
            DYNAMIC_LENGTH,  # fd
            DYNAMIC_LENGTH  # ff
        ]

        # TODO: This should really be 5.0.0.a
        if self.version >= Version(5, 0, 0, 0):
            self._packet_table[0x0B] = 0x07
            self._packet_table[0x16] = DYNAMIC_LENGTH
            self._packet_table[0x31] = DYNAMIC_LENGTH
        else:
            self._packet_table[0x0B] = 0x10A
            self._packet_table[0x16] = 0x01
            self._packet_table[0x31] = 0x01

        if self.version >= Version(5, 0, 9, 0):
            self._packet_table[0xE1] = DYNAMIC_LENGTH
        else:
            self._packet_table[0xE1] = 0x09

        if self.version >= Version(6, 0, 13, 0):
            self._packet_table[0xE3] = DYNAMIC_LENGTH
            self._packet_table[0xE6] = 0x05
            self._packet_table[0xE7] = 0x0C
            self._packet_table[0xE8] = 0x0D
            self._packet_table[0xE9] = 0x4B
            self._packet_table[0xEA] = 0x03
        else:
            self._packet_table[0xE3] = 0x4D
            self._packet_table[0xE6] = DYNAMIC_LENGTH
            self._packet_table[0xE7] = DYNAMIC_LENGTH
            self._packet_table[0xE8] = DYNAMIC_LENGTH
            self._packet_table[0xE9] = DYNAMIC_LENGTH
            self._packet_table[0xEA] = DYNAMIC_LENGTH

        if self.version >= Version(6, 0, 17, 0):
            self._packet_table[0x08] = 0x0F
            self._packet_table[0x25] = 0x15
        else:
            self._packet_table[0x08] = 0x0E
            self._packet_table[0x25] = 0x14

        if self.version >= Version(6, 0, 6, 0):
            self._packet_table[0xEE] = 0x2000
            self._packet_table[0xEF] = 0x2000
            self._packet_table[0xF1] = 0x09
        else:
            self._packet_table[0xEE] = DYNAMIC_LENGTH
            self._packet_table[0xEF] = 0x15
            self._packet_table[0xF1] = DYNAMIC_LENGTH

        if self.version >= Version(6, 0, 14, 2):
            self._packet_table[0xB9] = 0x05
        else:
            self._packet_table[0xB9] = 0x03

        if self.version >= Version(7, 0, 0, 0):
            self._packet_table[0xEE] = 0x0A // 0x2000
            self._packet_table[0xEF] = 0x15 // 0x2000
        else:
            self._packet_table[0xEE] = DYNAMIC_LENGTH
            self._packet_table[0xEF] = 0x15

        if self.version >= Version(7, 0, 9, 0):
            self._packet_table[0x24] = 0x09
            self._packet_table[0x99] = 0x1E
            self._packet_table[0xBA] = 0x0A
            self._packet_table[0xF3] = 0x1A
            self._packet_table[0xF1] = 0x09
            self._packet_table[0xF2] = 0x19
        else:
            self._packet_table[0x24] = 0x07
            self._packet_table[0x99] = 0x1A
            self._packet_table[0xBA] = 0x06
            self._packet_table[0xF3] = 0x18
            self._packet_table[0xF1] = DYNAMIC_LENGTH
            self._packet_table[0xF2] = DYNAMIC_LENGTH

        if self.version >= Version(7, 0, 18, 0):
            self._packet_table[0x00] = 0x6A
        else:
            self._packet_table[0x00] = 0x68

    def __getitem__(self, item) -> int:
        return self._packet_table[item]

    def is_dynamic_length(self, packet_id: int) -> bool:
        return self._packet_table[packet_id] == DYNAMIC_LENGTH


