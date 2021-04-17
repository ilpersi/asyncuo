import asyncio
import functools
import logging
import socket
import sys
import typing


from asyncuo.client import UOClient
from uo.client_version import Version


class AsyncUOProtocol(asyncio.Protocol):
    def __init__(self, loop: asyncio.AbstractEventLoop, version: str, shard_ip: str, shard_port: int = 2593,
                 seed: int = 42, log_level: int = logging.DEBUG, log_stream=sys.stdout):
        # print("_______________ INIT SERVER _______________")
        # asyncio.Protocol.__init__(self)

        # the asyncuo loop to be used
        self.loop: asyncio.AbstractEventLoop = loop
        # the client version to get the correct packet table
        self.version: Version = Version.from_string(version)
        # shard details
        self.shard_ip: str = shard_ip
        self.shard_port: int = shard_port
        # seed?
        self.__seed: int = seed

        # log management
        self._log_level: int = log_level
        self._log_stream = log_stream

        # other attributes used somewhere else
        self.transport: typing.Optional[asyncio.Transport] = None
        self.socket: typing.Optional[socket.socket] = None
        self.listen_ip: str = ''
        self.listen_port: int = -1
        self.buffer: list = list()
        self.client: typing.Optional[asyncio.Transport] = None
        self.address: typing.Optional[tuple] = None
        self.log: typing.Optional[logging.Logger] = None
        self.clients: dict = {}

    def connection_made(self, transport: asyncio.Transport):
        """Called when a connection is made.

        To receive data, wait for data_received() calls.
        When the connection is closed, connection_lost() is called.
        :param transport: the transport representing the pipe connection.
        """

        self.transport: asyncio.Transport = transport

        # we get additional info on the transport
        self.address = transport.get_extra_info('peername')
        self.socket = transport.get_extra_info('socket')

        # we set the TCP_NODELAY flag
        self.socket.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 0)

        # ip and port on which the server will listed
        self.listen_ip, self.listen_port = self.socket.getsockname()

        # we initialize the log
        if not self.log:
            logging.basicConfig(
                level=self._log_level,
                format='%(name)s: %(message)s',
                stream=self._log_stream,
            )

            self.log = logging.getLogger(
                'ServerProtocol_{}_{}'.format(*self.address)
            )

        self.log.debug('AsyncUOProtocol connection accepted')
        # print('connection accepted')

        # self.transport.write(struct.pack('>I', self.__seed))

    def connection_lost(self, error):
        """Called when the connection is lost or closed.

        :param error: is an exception object or None (the latter
        meaning a regular EOF is received or the connection was
        aborted or closed).
        """

        if error:
            self.log.error('AsyncUOProtocol connection_lost ERROR: {}'.format(error))
        else:
            self.log.debug('AsyncUOProtocol connection_lost closing')

            # A client has been initialized
            if self.client is not None:
                self.log.debug('Closing client....')

                peer_name = self.transport.get_extra_info('peername')

                if not self.client.transport.is_closing():
                    self.client.transport.close()
                if self.clients.get(peer_name):
                    del self.clients[peer_name]
                if self.client:
                    del self.client
                self.client = None

        # super().connection_lost(error)

    def data_received(self, data: bytes):
        """Called when some data is received.

        :param data: is  a bytes object.
        """

        # we get the UO packet command
        cmd = data[0]
        pkt_len = len(data)
        self.log.debug('AsyncUOProtocol data_received: packet {:#4X} len {}'.format(cmd, pkt_len))

        # ... And we forward it to the client
        asyncio.Task(self.send_data(data))

    async def send_data(self, data: bytes):
        """Called to forward data to the client.

        :param data: is  a bytes object.
        """

        # get a client by its peername as we do not want to have multiple connections to the same shard
        peer_name = self.transport.get_extra_info('peername')
        client_info = self.clients.get(peer_name)

        # in some circumstances the client has been initialized, but the protocol is still not ready
        # while client_info is not None and client_info.get('protocol') is None:
        while client_info is not None and client_info.get('protocol') is None:
            # self.log.debug('Waiting 0.01 seconds.')
            await asyncio.sleep(0.01)

        # creation of a new client protocol
        if client_info is None or not client_info['protocol'].connected:
            self.clients[peer_name] = dict(init=True, protocol=None, transport=None)
            client_factory = functools.partial(UOClient, version=self.version, loop=self.loop, server=self,
                                               log_level=self._log_level)
            client_transport, client_protocol = (None, None)
            client_transport, client_protocol = await self.loop.create_connection(client_factory,
                                                                                  self.shard_ip, self.shard_port)
            # we reference the server transport in the client protocol
            # client_protocol.server_transport = self.transport
            self.clients[peer_name]['protocol'] = client_protocol
            self.clients[peer_name]['transport'] = client_transport

        # self client is not None when the client is fully inizialized and connected
        if self.client is not None:
            # forward data to the client
            self.log.debug('AsyncUOProtocol client transport write: packet {:#4X}'.format(data[0]))
            self.client.transport.write(data)
            await asyncio.sleep(0.001)
        else:
            # we may recieve data when the client is not fully initialized, if this is the case we store it for later
            # usage
            self.buffer.append(data)
