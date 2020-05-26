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

from typing import Callable, Dict, List


class Observable:

    def __init__(self):
        self._observers: Dict[str, List[Callable]] = {}

    def add_observer(self, observer: Callable, prop: str = None):
        # prop=None means the caller is interested in observing all properties
        self._observers.setdefault(prop, []).append(observer)

    def remove_observer(self, observer: Callable, prop: str = None):
        # prop=None means the caller is not interested in any property anymore
        if prop:
            self._observers[prop].remove(observer)
        else:
            for prop, observers in self._observers.items():
               self._observers[prop] = [o for o in observers if o != observer]

    def notify_observers(self, prop: str = None):
        # always notify observers that observe all properties
        for observer in self._observers.get(None, []):
            observer(self, prop)
        if prop:
            for observer in self._observers.get(prop, []):
                observer(self)
 