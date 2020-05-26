#!/usr/bin/env python3
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

import threading
import time

from reaper import Client as ReaperClient
from component.fx import Fx
from component.fxparam import FxParameter
from component.transport import Transport
from component.track import Track


def transport_playing_updated(transport: Transport):
    print(f'playing = {transport.playing}')


def track_updated(track: Track, prop: str):
    print(f'{track.name} vol = {track.volume}dB; pan = {track.pan}; mute = {track.mute}; vu = {track.vu}')


def fx_updated(fx: Fx, prop: str):
    print(f'{fx.track.name}; {fx.name} bypass = {fx.bypass}')


def fx_param_updated(param: FxParameter, prop: str):
    print(f'{param.fx.track.name}; {param.fx.name}; param {param.n} = {param.value}')


def reaper_ready(reaper: ReaperClient):
    if not reaper.ready:
        return

    reaper.transport.add_observer(transport_playing_updated, prop='playing')
    
    for track in reaper.mixer.tracks:
        print(track.name)
        track.add_observer(track_updated)
        for fx in track.fx:
            print(f'  {fx.name}')
            fx.add_observer(fx_updated)
            for param in fx.parameters:
                print(f'    {param.n:2} = {param.value}')
                param.add_observer(fx_param_updated)

    threading.Thread(target=main_loop, args=(reaper,)).start()


def main_loop(reaper: ReaperClient):
    try:
        while True:
            time.sleep(1)
            val = input('\nType a new volume value in dB for track 1 and hit ⮐\n')
            try:
                reaper.mixer.get_track(1).volume = float(val)
                print('OK')
            except ValueError:
                print('Invalid value')
    except KeyboardInterrupt:
        reaper.disconnect()
        print('Bye!')


if __name__ == '__main__':
    print("Make sure REAPER OSC control surface mode is set to 'Local port'")
    print("and configured to listen on port 8000 (the default)\n")
    reaper = ReaperClient()
    reaper.add_observer(reaper_ready, prop='ready')
    reaper.connect()
