import asyncio
import functools
import logging
import socket
import struct
import time
import typing
import sys

import uo.packets

from uo.compression import Compression
from uo.packet_table import PacketTable
from uo.serialize import PacketReader, PacketWriter
from uo.client_version import Version


def split_by_n(seq, n):
    """A generator to divide a sequence into chunks of n units."""
    while seq:
        yield seq[:n]
        seq = seq[n:]


class UOClient(asyncio.Protocol):

    def __init__(self, loop: asyncio.AbstractEventLoop, server, version: Version,
                 log_level: int = logging.DEBUG,
                 log_stream=sys.stdout) -> None:
        # print("_______________ INIT CLIENT _______________")
        # the asyncio loop
        self.loop: asyncio.AbstractEventLoop = loop
        # the AsyncUOProtocol server instance
        self.server = server
        # is the UOClient instance connected to the shard?
        self.connected: bool = False
        # the client transport (initialized on connection_made)
        self.transport = None

        # packet management
        self.packet_table: PacketTable = PacketTable(version)
        self._compression: Compression = Compression()

        self.address = None

        # log management
        self.log: typing.Optional[logging.Logger] = None
        self._log_level: int = log_level
        self._log_stream = log_stream

        # network stuff
        self.socket: typing.Optional[socket.socket] = None
        self._input: bytes = bytes()
        self._packet_totals: typing.Optional[dict] = None
        self._packets_compression: bool = False
        if self.loop.client_decompress:
            self._packets_compression = True
            self.loop.client_decompress = False

        # what packets should the tool rewrite?
        self.rewriters: dict = {
            0x8C: functools.partial(RelayRewrite, original_ip=self.server.shard_ip, new_ip=self.server.listen_ip,
                                    original_port=self.server.shard_port, new_port=self.server.listen_port,
                                    packet_length=self.packet_table[0x8C]),
            0xA8: functools.partial(ServerListRewrite, original_ip=self.server.shard_ip, new_ip=self.server.listen_ip,
                                    packet_length=self.packet_table[0xA8]),
        }

        self.auto_answer: dict = {
            # 0xF0: functools.partial(RazorAnswer, transport=self.server.transport,
            #                         packet_length=self.packet_table[0xF0]),
        }

    def _packet_from_buffer(self) -> typing.Optional[PacketReader]:
        if len(self._input) == 0:
            return None

        cmd: int = self._input[0]

        if self.packet_table.is_dynamic_length(cmd):
            if len(self._input) < 3:
                packet_len: int = -1  # invalid buffer input
            else:
                packet_len: int = struct.unpack('!H', self._input[1:3])[0]
                if packet_len < 3 or packet_len > 0x8000:
                    packet_len: int = -2  # invalid dynamic packet length

                if len(self._input) < packet_len:
                    packet_len: int = -3  # wrong length

        else:
            packet_len: int = self.packet_table[cmd]

        if packet_len < 0:
            if packet_len == -1:
                self.log.error("Invalid buffer input for cmd {}".format(hex(cmd)))
            elif packet_len == -2:
                self.log.error("Invalid dynamic packet length for cmd {}".format(hex(cmd)))
            elif packet_len == -3:
                self.log.error("Wrong dynamic packet length for cmd {}".format(hex(cmd)))
            return None

        data_start: int = 3 if self.packet_table.is_dynamic_length(cmd) else 1
        data, self._input = self._input[data_start:packet_len], self._input[packet_len:]

        return PacketReader(cmd, data)

    def connection_made(self, transport: asyncio.WriteTransport):
        """Called when a connection is made.

        To receive data, wait for data_received() calls.
        When the connection is closed, connection_lost() is called.
        :param transport: the transport representing the pipe connection.
        """

        # we set the TCP_NODELAY flag
        self.socket = transport.get_extra_info('socket')
        self.socket.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 0)

        self.connected = True
        self._packet_totals = {'totals': 0}

        # save the transport
        self.transport = transport

        self.address = transport.get_extra_info('peername')

        if not self.log:
            logging.basicConfig(
                level=self._log_level,
                format='%(name)s: %(message)s',
                stream=self._log_stream,
            )

            self.log = logging.getLogger(
                'UOClient_{}_{}'.format(*self.address)
            )

            self.log.debug('Client connected to shard {}'.format(self.address))

        # we reference the client instance in the server one
        self.server.client = self

        # if some data is present in the buffer, we empty it
        if len(self.server.buffer) > 0:
            self.log.debug("Server buffer is not empty")
            for data in self.server.buffer:
                self.transport.write(data)
                time.sleep(0.001)
            self.server.buffer = list()

    def data_received(self, data: bytes):
        """Called when some data is received.

        :param data: is  a bytes object.
        """
        self.log.debug("Received {} bytes".format(len(data)))

        if self._packets_compression:
            # TODO Compression is not working at the moment
            original_data = data[:]
            compressed_data = data[:]
            uncompressed_data = self._compression.decompress(compressed_data)
            self._input += uncompressed_data
            new_compressed_data = self._compression.compress(uncompressed_data)

            self.log.debug("Uncompressed data is {} bytes".format(len(data)))

        else:
            self._input += data

        while True and not self._packets_compression:
            packet: PacketReader = self._packet_from_buffer()

            if packet is None:
                break

            if packet.cmd in self.auto_answer:
                self.log.debug('Auto answering packet {:#4x}'.format(packet.cmd))
                # answer = self.auto_answer[cmd](data=data)

            if packet.cmd in self.rewriters:
                self.log.debug('Rewriting packet {:#4x}'.format(packet.cmd))
                rewriter = self.rewriters[packet.cmd](packet=packet)
                packet_data = rewriter.to_data()
            else:
                new_packet = PacketWriter(packet.cmd, self.packet_table[packet.cmd])
                new_packet.data(packet.raw_data)
                packet_data = new_packet.finish()

            self.log.debug('UOClient data_received: packet {:#4X} len {}'.format(packet.cmd, len(packet_data)))

            # when we connect to the relay we turn decompression on
            if packet.cmd == 0x8C:
                self.loop.client_decompress = True

            # forward data to the client
            if not self._packets_compression:
                try:
                    self.server.transport.write(packet_data)
                    self.log.debug('UOClient serv transport write: packet {:#4X}'.format(packet.cmd))
                except Exception as e:
                    print("EXC {}".format(e))

        if self._packets_compression:
            try:
                self.server.transport.write(original_data)
                self.log.debug('UOClient serv transport write: compressed data')
            except Exception as e:
                print("EXC {}".format(e))

        # self._packet_totals['totals'] += 1
        # if not self._packet_totals.get(packet.cmd):
        #     self._packet_totals[packet.cmd] = 0
        # self._packet_totals[packet.cmd] += 1

    def connection_lost(self, error):
        """Called when the connection is lost or closed.

        :param error: is an exception object or None (the latter
        meaning a regular EOF is received or the connection was
        aborted or closed).
        """

        for k, v in self._packet_totals.items():
            if k != 'totals':
                self.log.debug("Packet {} -> cnt {}".format(hex(k), v))

        if error:
            self.log.debug("UOClient connection_lost ERROR: {}".format(error))
        else:
            self.log.debug('UOClient connection_lost closing with no error')

        self.connected = False

        # client_info clean up
        peer_name = self.server.transport.get_extra_info('peername')
        client_info = self.server.clients.get(peer_name)
        if client_info:
            if self.server.clients.get(peer_name):
                del self.server.clients[peer_name]
            if self.server.client:
                del self.server.client
            self.server.client = None

        self.log.info("Client connection lost")

        # some time connection is closed by the server, in this case we sure that no client is connected
        if not self.server.transport.is_closing():
            self.server.transport.close()


class RelayRewrite:
    def __init__(self, packet: PacketReader, original_ip: str, new_ip: str, original_port: int, new_port: int,
                 packet_length: int):

        self.packet_length = packet_length

        self._logger = logging.getLogger(
            'RelayRewrite'
        )

        # sometimes servers return longer packet length
        self.p = packet
        self.relay = uo.packets.Relay(self.p)

        if self.relay.ip == original_ip:
            self.relay.ip = new_ip
        else:
            self._logger.warning("RelayRewrite IP: {} -> Original: {}".format(self.relay.ip, original_ip))

        if self.relay.port == original_port:
            self.relay.port = new_port
        else:
            self._logger.warning("RelayRewrite Port: {} -> Original: {}".format(self.relay.port, original_port))

    def to_data(self):
        packet = PacketWriter(0x8C, self.packet_length)
        packet.ipv4(self.relay.ip)
        packet.ushort(self.relay.port)
        packet.uint(self.relay.auth_id)

        return packet.finish()


class ServerListRewrite:
    def __init__(self, packet: PacketReader, original_ip: str, new_ip: str, packet_length: int):
        self.p = packet
        self.server_list = uo.packets.ServerList(self.p)
        self.packet_length = packet_length

        for server in self.server_list.servers:
            if server.ip == original_ip:
                server.ip = new_ip

    def to_data(self):
        packet = PacketWriter(0xA8, self.packet_length)
        packet.byte(self.server_list.sys_info_flag)
        packet.ushort(self.server_list.count)

        for server in self.server_list.servers:
            packet.ushort(server.index)
            packet.fixstring(server.name, 32)
            packet.byte(server.percent_full)
            packet.byte(server.timezone)
            packet.ipv4(server.ip, True)

        return packet.finish()


class RazorAnswer:
    def __init__(self, data: bytes, transport: asyncio.WriteTransport, packet_length: int):
        self.data: bytes = data[:]
        self.p: uo.packets.UOPacket = uo.packets.UOPacket(self.data, packet_length)
        self.packet_length = packet_length
        self.razor_features = uo.packets.RazorFeatures(self.p.from_buffer())

        if self.razor_features.features == 0xFE:
            packet = PacketWriter(0xF0, packet_length)
            packet.ushort(0x0004)
            packet.byte(0xFF)
            transport.write(packet.finish())
