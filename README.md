# pyreaosc

Python 3 based implementation of an object-oriented API for controlling and monitoring some REAPER mixer features. Leverages the built-in OSC control surface so no additional DAW-side extensions are required. Works on Windows, macOS and Linux.

#### Example

    from reaper import Client as ReaperClient

    def reaper_ready(reaper):
      reaper.mixer.get_track(1).volume = 6.0
      reaper.transport.play()

    reaper = ReaperClient()
    reaper.add_observer(reaper_ready, prop='ready')
    reaper.connect()


#### Features

- Transport play and record status
- Track volume, pan and mute
- FX bypass
- FX parameter values


#### Setup

- REAPER → Preferences → Control/OSC/web → Add → OSC → Mode "Local port"
- Add one or more tracks with some FXs
- Run `example.py` and follow instructions for a control demo
- Tweak volume, mute, plugins... for a feedback demo

