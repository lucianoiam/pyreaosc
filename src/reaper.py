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

from base import window
from base.channel import OscChannel
from base.component import Component
from base.types import OscArgument
from component.mixer import Mixer
from component.transport import Transport


class Client(Component):

    def __init__(self, host: str = '127.0.0.1', port: int = 8000):
        super().__init__(channel=OscChannel(host=host, port=port, handler=self.handle_osc))
        self._ready = False
        self._mixer = Mixer(parent=self)
        self._transport = Transport(parent=self)

    @property
    def ready(self) -> bool:
        return self._ready

    @property
    def mixer(self) -> Mixer:
        return self._mixer
    
    @property
    def transport(self) -> Transport:
        return self._transport

    def connect(self):
        self.channel.connect()
        # Control surface: refresh all surfaces
        # ready property will be set to true after parsing response:
        self.send_action(41743)

    def disconnect(self):
        self.channel.disconnect()
        self.set_prop('ready', False)

    def focus_main_window(self):
        try:
            window.focus('REAPER')
        except Exception as e:
            print(f'Cannot focus main window: {e}')

    def handle_osc(self, path: str, *args: OscArgument):
        if not self._ready and path.startswith('/lastregion'):
            # assume last message triggered by action 41743 is /lastregion
            self.set_prop('ready', True)
            return

        if self._mixer.handle_osc(path, *args):
            return

        if self._transport.handle_osc(path, *args):
            return
