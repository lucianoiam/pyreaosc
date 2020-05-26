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

from base.component import RootComponent
from base.types import OscArgument


class Transport(RootComponent):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._playing = False
        self._recording = False

    @property
    def playing(self) -> bool:
        return self._playing

    @property
    def recording(self) -> bool:
        return self._recording

    def play(self):
        self.send_osc('/play')

    def record(self):
        self.send_osc('/record')

    def stop(self):
        self.send_osc('/stop')

    def go_to_end(self):
        """Transport: Go to end of project"""
        self.send_action(40043)

    def arm_all_tracks(self):
        """Track: Arm all tracks for recording"""
        self.send_action(40490)

    def unarm_all_tracks(self):
        """Track: Unarm all tracks for recording"""
        self.send_action(40491)

    def forward_one_measure(self):
        """Move edit cursor forward one measure (no seek)"""
        self.send_action(40839)

    def handle_osc(self, path: str, *args: OscArgument) -> bool:
        if path == '/play':
            self.set_prop('playing', args[0] == 1.0)
            return True

        elif path == '/record':
            self.set_prop('recording', args[0] == 1.0)
            return True
            
        return False
