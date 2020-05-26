"""
    Copyright © 2020 Luciano Iam <lucianito@gmail.com>

    This library is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This library is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this library.  If not, see <https://www.gnu.org/licenses/>.
"""

import socket
import sys

from threading import Thread
from typing import Callable

from pythonosc import dispatcher, osc_message_builder, osc_server, udp_client
from .types import OscArgument


class OscChannel:

    def __init__(self, host: str, port: int, handler: Callable):
        self._host = host
        self._port = port
        
        self._dispatcher = dispatcher.Dispatcher()
        self._dispatcher.set_default_handler(handler)

        self._udp_client: udp_client.UDPClient = None

    def connect(self):
        # https://github.com/attwad/python-osc/issues/41
        self._udp_client = udp_client.UDPClient(self._host, self._port)
        self._udp_client._sock.bind(('', 0))

        osc_server.BlockingOSCUDPServer.allow_reuse_address = True

        if sys.platform == 'linux':
            self._udp_client._sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        _, src_port = self._udp_client._sock.getsockname()

        self._udp_server = osc_server.BlockingOSCUDPServer((self._host, src_port), self._dispatcher)

        Thread(target=self._udp_server.serve_forever, name='reaper_osc').start()

    def disconnect(self):
        self._udp_server.shutdown()

    def send(self, path: str, *args: OscArgument):
        builder = osc_message_builder.OscMessageBuilder(address=path)

        for arg in args:
            builder.add_arg(arg)
        
        self._udp_client.send(builder.build())
