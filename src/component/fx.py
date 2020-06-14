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
from .fxparam import FxParameter


class Fx(ChildComponent):

    def __init__(self, n: int, name: str, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._n = n
        self._name = name
        self._bypass = False
        self._parameters: List = []

    @property
    def track(self):
        return self.parent

    @property
    def n(self) -> int:
        return self._n

    @property
    def name(self) -> str:
        return self._name

    @property
    def bypass(self) -> bool:
        return self._bypass
    
    @bypass.setter
    def bypass(self, value: bool):
        self._bypass = value
        self.send_osc(f'/track/{self.track.n}/fx/{self.n}/bypass', 0.0 if value else 1.0)

    @property
    def parameters(self) -> List:
        return self._parameters

    def has_parameter(self, n: int) -> bool:
        return n <= len(self._parameters)

    def get_parameter(self, n: int) -> FxParameter:
        return self._parameters[n - 1]

    def handle_osc(self, path: str, *args: OscArgument) -> bool:
        m = re.search(r'/track/\d+/fx/\d+/bypass', path)
        if m:
            # seems to be reversed
            self.set_prop('bypass', args[0] == 0)
            return True

        """server does not report name for fxparams in tracks
           hence there is no way to determine if a param exists at all
           create a new param when a /value message is received
        """

        m = re.search(r'/track/\d+/fx/\d+/fxparam/(\d+)/value', path)
        if m:
            param_n = int(m.group(1))
            if self.has_parameter(param_n):
                return self.get_parameter(param_n).handle_osc(path, *args)
            else:
                param = FxParameter(n=param_n, name=None, value=args[0], parent=self)
                self._parameters.append(param)
                self.notify_observers('parameters')
                return True

        return False
