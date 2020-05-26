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

from base.component import Component
from base.types import OscArgument


class FxParameter(Component):

    def __init__(self, fx, n: int, name: str, value: float, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._fx = fx
        self._n = n
        self._name = name
        self._value = value

    @property
    def fx(self):
        return self._fx

    @property
    def n(self) -> int:
        return self._n

    @property
    def name(self) -> str:
        return self._name
    
    @property
    def value(self) -> float:
        return self._value
    
    @value.setter
    def value(self, value: float):
        self._value = value
        self.send_osc(f'/track/{self.fx.track.n}/fx/{self.fx.n}/fxparam/{self.n}/value', float(value))

    def handle_osc(self, path: str, *args: OscArgument) -> bool:
        m = re.search(r'/track/\d+/fx/\d+/fxparam/\d+/value', path)
        if m:
            self.set_prop('value', args[0])
            return True

        return False
