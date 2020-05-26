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

from base.component import RootComponent
from base.types import OscArgument
from .track import Track


class Mixer(RootComponent):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._tracks: List[Track] = []

    @property
    def tracks(self) -> List[Track]:
        return self._tracks

    def has_track(self, n: int) -> bool:
        return n <= len(self._tracks)

    def get_track(self, n: int) -> Track:
        return self._tracks[n - 1]

    def handle_osc(self, path: str, *args: OscArgument) -> bool:
        """PEP 572 - Python 3.8+
           if m := re.search('/track/(\d+)/(.+)', path):
              track_n = ...
        """
        m = re.search(r'/track/(\d+)/(.+)', path)
        if m:
            track_n = int(m.group(1))
            if m.group(2) == 'name':
                # create track
                if args[0]:
                    self._tracks.append(Track(n=track_n, name=args[0], parent=self))
                    self.notify_observers('tracks')
                    return True
            else:
                # delegate message to existing track
                if self.has_track(track_n):
                    return self.get_track(track_n).handle_osc(path, *args)

        return False
