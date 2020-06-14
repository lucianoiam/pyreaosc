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

import re

from typing import List

from base.component import ChildComponent
from base.types import OscArgument
from .fx import Fx


class Track(ChildComponent):

    def __init__(self, n: int, name: str, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._n = n
        self._name = name
        self._volume: float = 0
        self._pan: float = 0
        self._mute = False
        self._vu: float = 0
        self._fx: List = []

    @property
    def n(self) -> int:
        return self._n

    @property
    def name(self) -> str:
        return self._name

    @property
    def volume(self) -> float:
        return self._volume
    
    @volume.setter
    def volume(self, value: float):
        self._volume = value
        self.send_osc(f'/track/{self.n}/volume/db', float(value))

    @property
    def pan(self) -> float:
        return self._pan
    
    @pan.setter
    def pan(self, value: float):
        self._pan = value
        self.send_osc(f'/track/{self.n}/pan', float(value))

    @property
    def mute(self) -> bool:
        return self._mute
    
    @mute.setter
    def mute(self, value: bool):
        self._mute = value
        self.send_osc(f'/track/{self.n}/mute', 1.0 if value else 0.0)

    @property
    def vu(self) -> float:
        return self._vu

    @property
    def fx(self) -> List:
        return self._fx

    def has_fx(self, n: int) -> bool:
        return n <= len(self._fx)

    def get_fx(self, n: int) -> Fx:
        return self._fx[n - 1]

    def handle_osc(self, path: str, *args: OscArgument) -> bool:
        m = re.search(r'/track/\d+/vu', path)
        if m:
            self.set_prop('vu', args[0])
            return True

        m = re.search(r'/track/\d+/fx/(\d+)/(.+)', path)
        if m:
            fx_n = int(m.group(1))
            if m.group(2) == 'name':
                if args[0]:
                    self._fx.append(Fx(n=fx_n, name=args[0], parent=self))
                    self.notify_observers('fx')
            else:
                if self.has_fx(fx_n):
                    return self.get_fx(fx_n).handle_osc(path, *args)
            return True

        m = re.search(r'/track/\d+/(.+)', path)
        if m:
            subpath = m.group(1)
            if subpath == 'volume/db':
                self.set_prop ('volume', args[0])
            elif subpath == 'pan':
                self.set_prop ('pan', args[0])
            elif subpath == 'mute':
                self.set_prop ('mute', args[0] != 0.0)
            return True

        return False
