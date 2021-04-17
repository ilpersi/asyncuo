#!/usr/bin/python3

import asyncio
import argparse
import functools
import logging
import sys

import asyncuo.server


parser = argparse.ArgumentParser(description='Creates a proxy for UO.')
parser.add_argument('-li', '--listen-ip', type=str, default='127.0.0.1',
                    help='the IP on which the ASyncUO tool should run')
parser.add_argument('-lp', '--listen-port', type=int, required=True,
                    help='the port on which the ASyncUO tool should listen for incoming connection')
parser.add_argument('-si', '--shard-ip', type=str, required=True,
                    help='the IP of the shard to connect to')
parser.add_argument('-sp', '--shard-port', type=int, required=True,
                    help='the port of the shard to connect to')
parser.add_argument('-ll', '--log-level', type=int, default=logging.DEBUG,
                    help='the log level')
parser.add_argument('-cv', '--client-version', type=str, required=True, default="7.0.58.9",
                    help='UO Client Version')

args = parser.parse_args()

logging.basicConfig(
    level=args.log_level,
    format='%(name)s: %(message)s',
    stream=sys.stdout,
)
log = logging.getLogger('main')

event_loop = asyncio.get_event_loop()
# this one is set to true from the client after a shard has been choosen from the list
# placing it here is a workaround to be sure that the status is not lost when server or client is restarted
event_loop.client_decompress = False

# Create the server and let the loop finish the coroutine before
# starting the real event loop.

server_factory = functools.partial(asyncuo.server.AsyncUOProtocol, version=args.client_version,
                                   seed=42, loop=event_loop, shard_ip=args.shard_ip, shard_port=args.shard_port,
                                   log_level=args.log_level)

coro = event_loop.create_server(server_factory, args.listen_ip, args.listen_port)
server = event_loop.run_until_complete(coro)
log.debug('Client version is "{}"'.format(args.client_version))
log.debug('Starting up on {} port {}'.format(args.listen_ip, args.listen_port))
log.debug('Shard on {} port {}'.format(args.shard_ip, args.shard_port))

# Enter the event loop permanently to handle all connections.
for x in server.sockets:
    print('Serving on {}'.format(x.getsockname()))
try:
    event_loop.run_forever()
except KeyboardInterrupt:
    log.debug("Keboard Interrupt")
finally:
    log.debug('closing server')
    server.close()
    event_loop.run_until_complete(server.wait_closed())
    log.debug('closing event loop')
    event_loop.close()
