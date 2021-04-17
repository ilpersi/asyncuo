#!/usr/bin/env python
import struct
from twisted.internet import protocol, reactor

LISTEN_PORT = 33604
SHARD_PORT = 2593
SHARD_ADDR = "127.0.0.1"
SHARD_ADDR = "34.234.30.69"  # Demise


def split_by_n(seq, n):
    """A generator to divide a sequence into chunks of n units."""
    while seq:
        yield seq[:n]
        seq = seq[n:]


class ServerProtocol(protocol.Protocol):
    def __init__(self):
        self.buffer = bytes()
        self.client = None

    def connectionMade(self):
        protocol.Protocol.connectionMade(self)
        
        factory = protocol.ClientFactory()
        factory.protocol = ClientProtocol
        factory.server = self

        reactor.connectTCP(SHARD_ADDR, SHARD_PORT, factory)
    
    # Client => Proxy
    def dataReceived(self, data):
        if self.client is not None:
            # print('Client => Proxy (client) ' + data.encode('hex'))
            self.client.write(data)
        else:
            # if data[0].encode('hex') != 'ef':
            # print('Client => Proxy (no client) ' + data.encode('hex'))
            self.buffer += data

    # Proxy => Client
    def write(self, data):
        self.transport.write(data)
        # print 'Proxy => Client: ' + data.encode('hex')


class ClientProtocol(protocol.Protocol):
    def connectionMade(self):
        protocol.Protocol.connectionMade(self)
        self.transport.setTcpNoDelay(False)
        
        self.factory.server.client = self
        if self.factory.server.buffer:
            self.write(self.factory.server.buffer)
            self.factory.server.buffer = ''
            
    def connectionLost(self, reason=None):
        protocol.Protocol.connectionLost(self, reason)
        print("connectionLost", repr(reason))

    # Server => Proxy
    def dataReceived(self, data):
        # print 'Server => Proxy: ' + data.encode('hex')

        # print('host: {}'.format(self.factory.server.transport.getHost().host))
        if data[0] == 0xa8:
            print('Rewriting 0xa8')
            server_num = struct.unpack_from('!H', data, 4)[0]
            # print('server_num: {}'.format(server_num))

            if server_num > 0:
                # we get the ip of the machine running the server and 
                # we convert it to the uo format -> no dots, reverted
                my_ip = str(self.factory.server.transport.getHost().host).split('.')[::-1]
                my_ip_str = bytes((int(x) for x in my_ip))

                # we do the same for the shard addres
                shard_ip = SHARD_ADDR.split('.')[::-1]
                shard_ip_str = bytes((int(x) for x in shard_ip))

                # some prints
                # print('my_ip : {} my_ip_str: {}'.format(my_ip, my_ip_str))
                # print('shard_ip : {} shard_ip_str: {}'.format(shard_ip, shard_ip_str))

                # we skip the first five bytes and loop on server records
                servers = [x for x in split_by_n(data[6:], 40)]
                for server in servers:
                    ip = server[-4:]
                    if ip == shard_ip_str:
                        # print('found match')
                        data = data.replace(ip, my_ip_str)
                        # print(data_new.encode('hex'))

        if data[0] == 0x8c:
            # we get the ip of the machine running the proxy and we format it
            my_ip = str(self.factory.server.transport.getHost().host).split('.')
            my_ip_str = bytes((int(x) for x in my_ip))

            # we do the same for the shard addres
            shard_ip = SHARD_ADDR.split('.')
            shard_ip_str = bytes((int(x) for x in shard_ip))

            ip = data[1:5]
            # print('my_ip_str {} shard_ip_str {} ip {}'.format(my_ip_str.encode('hex'), shard_ip_str.encode('hex'), ip.encode('hex')))
            if ip == shard_ip_str:
                # print('match found')
                print('Rewriting 0x8c')
                data = data.replace(ip, my_ip_str)
                # print(data.encode('hex'))

            # we create a string for the shard port
            shard_port_str = struct.pack('!H', SHARD_PORT)

            my_port_str = struct.pack('!H', LISTEN_PORT)

            port = data[5:7]
            # print('port {}'.format(port.encode('hex')))
            if port == shard_port_str:
                data = data.replace(port, my_port_str)
            
        if data[0] == 0xf0:
            print("Razor Feature Negotation")

        self.factory.server.write(data)
        
    # Proxy => Server
    def write(self, data):
             
        # print 'Proxy => Server: ' + data.encode('hex')
        self.transport.write(data)


def main():
    import sys
    from twisted.python import log

    log.startLogging(sys.stdout)

    factory = protocol.ServerFactory()
    factory.protocol = ServerProtocol

    reactor.listenTCP(LISTEN_PORT, factory)
    reactor.run()


if __name__ == '__main__':
    main()
