#!/usr/bin/env python
import time
import Live

from _Framework.ControlSurface import ControlSurface
from _Framework.EncoderElement import EncoderElement
from _Framework.InputControlElement import *
from _Framework.MixerComponent import MixerComponent
from _Framework.ViewControlComponent import ViewControlComponent
from _Framework.ButtonElement import ButtonElement

# Globals
mixer = None
view = None
mode_absolute = Live.MidiMap.MapMode.absolute

# Constants
CHANNEL = 0
NUM_SENDS = 4
SEND_A = 17
SEND_B = 18
SEND_C = 19
SEND_D = 20
PAN = 21
BUTTON_NEXT = 29
BUTTON_PREV = 31


class KontrolX1(ControlSurface):
    __module__ = __name__
    __doc__ = " Traktor Kontrol X1 (MK1) Control Script "

    def log(self, message):
        timestamp = time.strftime("%d.%m.%Y %H:%M:%S", time.localtime())
        self.log_message(timestamp, message)

    def __init__(self, c_instance):
        ControlSurface.__init__(self, c_instance)
        self._set_suppress_rebuild_requests(True)
        with self.component_guard():
            self.__c_instance = c_instance
            self.log("INIT JPS Kontrol")
            self.setup_mixer()
            self.setup_view()
        self._set_suppress_rebuild_requests(False)

    def setup_mixer(self):
        global mixer
        mixer = MixerComponent(2, 2)
        mixer.set_track_offset(0)
        self.song().view.selected_track = mixer.channel_strip(0)._track  # set the selected strip to the first track, so that we don't, for example, try to assign a button to arm the master track, which would cause an assertion error
        send_a = EncoderElement(MIDI_CC_TYPE, CHANNEL, SEND_A, mode_absolute)
        send_b = EncoderElement(MIDI_CC_TYPE, CHANNEL, SEND_B, mode_absolute)
        send_c = EncoderElement(MIDI_CC_TYPE, CHANNEL, SEND_C, mode_absolute)
        send_d = EncoderElement(MIDI_CC_TYPE, CHANNEL, SEND_D, mode_absolute)
        pan = EncoderElement(MIDI_CC_TYPE, CHANNEL, PAN, mode_absolute)
        mixer.selected_strip().set_send_controls([send_a, send_b, send_c, send_d])
        mixer.selected_strip().set_pan_control(pan)

    def setup_view(self):
        is_momentary = True
        global view
        view = ViewControlComponent()
        view.set_next_track_button(ButtonElement(is_momentary, MIDI_CC_TYPE, CHANNEL, BUTTON_NEXT))
        view.set_prev_track_button(ButtonElement(is_momentary, MIDI_CC_TYPE, CHANNEL, BUTTON_PREV))

    def _on_selected_track_changed(self):
        ControlSurface._on_selected_track_changed(self)
        selected_track = self.song().view.selected_track
        mixer.channel_strip(0).set_track(selected_track)
        all_tracks = ((self.song().tracks + self.song().return_tracks) + (self.song().master_track,))
        index = list(all_tracks).index(selected_track)
        self.log("selected track changed {}".format(index))

    def disconnect(self):
        self.log_message("CLEAN JPS Kontrol")
        ControlSurface.disconnect(self)
        return None
