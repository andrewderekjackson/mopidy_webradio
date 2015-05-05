import RPi.GPIO as GPIO
import logging

from mopidy import core

logger = logging.getLogger(__name__)

class ButtonController():

    def __init__(self, frontend):
        self.frontend = frontend

        GPIO.setmode(GPIO.BCM)
        GPIO.setup(4, GPIO.IN)
        GPIO.setup(17, GPIO.IN)
        GPIO.setup(27, GPIO.IN)

        GPIO.add_event_detect(4, GPIO.RISING, callback=self.button1_clicked, bouncetime=250)
        GPIO.add_event_detect(17, GPIO.RISING, callback=self.button2_clicked, bouncetime=250)
        GPIO.add_event_detect(27, GPIO.RISING, callback=self.button3_clicked, bouncetime=250)

    def button1_clicked(self, channel):

        l = self.frontend.core.playlists.as_list().get();
        for p in l:
            logger.info(p)

        pl = self.frontend.core.playlists.get_items("spotify:user:1230911936:playlist:3D6ADKqTJ4QnC0fEqnWqGW").get()

        logger.info(pl)

        self.frontend.core.tracklist.clear()
        self.frontend.core.tracklist.add(pl)


    def button2_clicked(self, channel):
        logger.info("Button 2 clicked.")
        pass

    def button3_clicked(self, channel):
        logger.info("Button 3 clicked.")

        c = self.frontend.core.playback

        current_state = c.get_state().get()

        logger.info("state is: " + current_state)

        if current_state == core.PlaybackState.STOPPED:
            c.play()
        else:
            if current_state == core.PlaybackState.PAUSED:
                c.resume()
            else:
                if current_state == core.PlaybackState.PLAYING:
                    c.pause()


        logger.info("new state is: " + c.get_state().get())
