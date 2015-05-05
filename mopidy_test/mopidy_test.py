# -*- coding: utf-8 -*-
import pykka, logging
import time

from .button_controller import ButtonController
import lcd
from rotary_encoder import RotaryEncoder
from lcd import LcdController
from mopidy import core

import os,operator

logger = logging.getLogger(__name__)

ROTARY_PIN_A = 14  # Pin 8
ROTARY_PIN_B = 15  # Pin 10
ROTARY_BUTTON = 4  # Pin 7

LONG_PRESS_TIME = 0.3

class TestFrontend(pykka.ThreadingActor, core.CoreListener):

    def __init__(self, config, core):
        super(TestFrontend, self).__init__()
        self.core = core

        self.lcd = LcdController()
        self.rotary = RotaryEncoder(ROTARY_PIN_A, ROTARY_PIN_B, ROTARY_BUTTON, self.switch_event)
        self.down_time_button = time.time()
        self._now_playing_track = None

        logger.info("My plugin has loaded!")

        # set up fallback image
        self.plugin_dir = os.path.dirname(os.path.realpath(__file__))
        logger.info("Current directory is " + self.plugin_dir)
        self.fallback_image = self.plugin_dir + "/images/on_the_air.jpg"
        logger.info("Fallback image is " + self.fallback_image)

        self.lcd.message("Internet Radio (Loading)")

    # This is the event callback routine to handle events
    def switch_event(self, event):
        if event == RotaryEncoder.CLOCKWISE:

            current_volume = self.core.mixer.get_volume().get()
            logger.info("Current volume: " + str(current_volume))

            current_volume += 5

            if current_volume > 100:
                current_volume = 100

            self.core.mixer.set_volume(current_volume)
            logger.info("New volume: " + str(current_volume))

        elif event == RotaryEncoder.ANTICLOCKWISE:
            current_volume = self.core.mixer.get_volume().get()
            logger.info("Current volume: " + str(current_volume))

            current_volume -= 5

            if current_volume < 0:
                current_volume = 0

            self.core.mixer.set_volume(current_volume)
            logger.info("New volume: " + str(current_volume))

        elif event == RotaryEncoder.BUTTONDOWN:
            self.toggle_play()

        return

    def toggle_play(self):

        current_state = self.core.playback.get_state().get()

        logger.info("state is: " + current_state)

        if current_state == core.PlaybackState.STOPPED:

            l = self.core.tracklist.get_length().get()
            logger.info(l)

            if l == 0:
                logger.info("Loading default playlist")
                self.load_playlist()

            current_state = self.core.playback.get_state().get()
            logger.info("state is: " + current_state)

            logger.info("Playing")

            self.core.playback.play()

        else:
            if current_state == core.PlaybackState.PAUSED:
                self.core.playback.resume()
            else:
                if current_state == core.PlaybackState.PLAYING:
                    self.core.playback.pause()

        logger.info("new state is: " + self.core.playback.get_state().get())

    def playlists_loaded(self):
        self.lcd.message("Internet Radio")

    def load_playlist(self):

        pl = self.core.playlists.lookup("spotify:user:1230911936:playlist:04OMIJJH2YSLkeVl5jhXjl").get()
        logger.info(pl)

        self.core.tracklist.clear()
        self.core.tracklist.add(pl.tracks)

        self.core.tracklist.set_random(True)

    def show_now_playing(self, track):

        # store for later
        self._now_playing_track = track

        logger.info(track)

        name = track.name
        artists = ', '.join([a.name for a in track.artists])

        track_image_uri = self.fallback_image

        if len(track.album.images) > 0:
            logger.info("Has an image...")

            track_image_uri = iter(track.album.images).next()
            logger.info("Image: %s",  track_image_uri)

        else:
            logger.info("Checking for image...")
            image_result = self.core.library.get_images({track.uri}).get()

            logger.info(image_result[track.uri])

            for image in image_result[track.uri]:
                if image.width >= 640:
                    logger.info("Found image: " + image.uri)
                    track_image_uri = image.uri

        logger.info("Playback started: %s - %s",  name, artists)
        logger.info("Name: %s", name)
        logger.info("Artists: %s",  artists)
        logger.info("Image: %s",  track_image_uri or "None")

        track_image_path = self.fallback_image
        if track_image_uri is not None:
            try:
                logger.info("Downloading image..." + track_image_uri)

                import tempfile
                temp_dir = tempfile.gettempdir()

                import urllib
                testfile = urllib.URLopener()

                track_image_path = temp_dir + "/art.jpg"
                logger.info("Saving to " + track_image_path)
                testfile.retrieve(track_image_uri, track_image_path)

                logger.info(image)

            except Exception as ex:
                logger.error("Error downloading image ...")
                logger.error(ex)

        logger.info("Updating LCD")
        self.lcd.now_playing(track_image_path, name.encode("utf8","ignore") or "", artists.encode("utf8","ignore") or "")


    def track_playback_started(self, tl_track):
        logger.info("STARTED")
        self.show_now_playing(tl_track.track)
        #self.lcd.message("Playing")

    def track_playback_paused(self, tl_track, time_position):
        logger.info("PAUSED")
        self.lcd.message("Paused")

    def track_playback_resumed(self, tl_track, time_position):
        logger.info("RESUMED")
        self.show_now_playing(tl_track.track)
        #self.lcd.message("Playing")

    def track_playback_ended(self, tl_track, time_position):
        logger.info("ENDED")
        # self.lcd.message("Stopped (Finished)")

    def volume_changed(self, volume):
        #self.lcd.message("Volume: " + str(volume))
        pass

    def stream_title_changed(self, title):
        pass
        #self.lcd.now_playing(self.fallback_image, title, "")
