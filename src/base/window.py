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

import sys

if sys.platform == 'darwin':
    import applescript
    import psutil
elif sys.platform == 'win32':
    import win32gui
    import re


def focus(name: str):
    if sys.platform == 'darwin':
        # applescript hangs if target app not running
        for proc in psutil.process_iter():
            if proc.name() == name:
                applescript.run(f'tell application "{name}" to activate')
                return

        raise Exception(f'Could not find application {name}')

    elif sys.platform == 'win32':
        # https://stackoverflow.com/questions/1888863/how-to-get-main-window-handle-from-process-id
        wmgr = WindowMgr()
        wmgr.find_window_wildcard(f'.*{name}.*')
        wmgr.set_foreground()
    
    else:
        raise Exception('Unsupported platform')


"""
   From StackOverflow, CC-BY-SA 4.0 license
   https://stackoverflow.com/questions/2090464/python-window-activation
"""

class WindowMgr:
    """Encapsulates some calls to the winapi for window management"""

    def __init__ (self):
        """Constructor"""
        self._handle = None

    def find_window(self, class_name, window_name=None):
        """find a window by its class_name"""
        self._handle = win32gui.FindWindow(class_name, window_name)

    def _window_enum_callback(self, hwnd, wildcard):
        """Pass to win32gui.EnumWindows() to check all the opened windows"""
        if re.match(wildcard, str(win32gui.GetWindowText(hwnd))) is not None:
            self._handle = hwnd

    def find_window_wildcard(self, wildcard):
        """find a window whose title matches the wildcard regex"""
        self._handle = None
        win32gui.EnumWindows(self._window_enum_callback, wildcard)

    def set_foreground(self):
        """put the window in the foreground"""
        win32gui.SetForegroundWindow(self._handle)
