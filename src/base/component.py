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

from .channel import OscChannel
from .observable import Observable
from .types import OscArgument


class Component(Observable):

    def __init__(self, parent):
        super().__init__()
        self._parent = parent

    @property
    def channel(self) -> OscChannel:
        return self._parent.channel
    
    def send_osc(self, path: str, *args: OscArgument):
        self.channel.send(path, *args)

    def send_action(self, action_id: int):
        self.send_osc('/action', action_id)

    def handle_osc(self, path: str, *args: OscArgument) -> bool:
        return False

    def set_prop (self, prop: str, value):
        if getattr(self, f'_{prop}') == value:
            return
        setattr(self, f'_{prop}', value)
        self.notify_observers(prop)


class RootComponent(Component):

    def __init__(self, channel: OscChannel):
        super().__init__(None)
        self._channel = channel

    @property
    def channel(self) -> OscChannel:
        return self._channel
