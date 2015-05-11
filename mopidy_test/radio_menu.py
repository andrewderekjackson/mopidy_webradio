# for menu
import threading
from lcd_menu import Command, MenuItem, DynamicMenuItem, Menu

import os
from time import time

# Rotary encoder
from rotary_encoder import RotaryEncoder
from lcd import Lcd

ROTARY_PIN_A = 14  # Pin 8
ROTARY_PIN_B = 15  # Pin 10
ROTARY_BUTTON = 4  # Pin 7


class RadioMenu(Menu):
    '''An example menu which received input from keyboard and outputs to a ILI9341 TFT display.'''

    MAIN_TITLE = "Internet Radio"

    def __init__(self, lcd_screen, plugin):

        self.lcd = lcd_screen
        self.rotary_encoder = RotaryEncoder(ROTARY_PIN_A, ROTARY_PIN_B, ROTARY_BUTTON, self.rotary_encoder_event)
        self.plugin = plugin

        # our example menu definition
        items = [
            MenuItem("Favorites", [
                Command("Andrew's Mix", self.plugin.load_playlist_and_play, "spotify:user:1230911936:playlist:04OMIJJH2YSLkeVl5jhXjl")
            ]),
            DynamicMenuItem("Browse", self.plugin.menu_load_playlists, None)
        ]

        # pass all this to the base class
        return super(RadioMenu, self).__init__(items, self.update)

    def rotary_encoder_event(self, event):

        if event == RotaryEncoder.CLOCKWISE:
            if self.showing_menu:
                print "MENU: DOWN"
                self.down()
            else:
                print "VOLUME: UP"
                self.plugin.volume_up()

        elif event == RotaryEncoder.ANTICLOCKWISE:
            if self.showing_menu:
                print "MENU: UP"
                self.up()
            else:
                print "VOLUME: DOWN"
                self.plugin.volume_down()

        elif event == RotaryEncoder.BUTTON_PRESSED:
            if self.showing_menu:
                print "MENU: SELECT"
                self.select()
            else:
                print "PLAY/PAUSE"
                self.plugin.toggle_play()

        elif event == RotaryEncoder.BUTTON_LONG_PRESSED:
            if self.showing_menu:
                print "MENU: BACK"
                self.back()
            else:
                print "MENU: SHOW"
                self.show()

        return

    def loading(self):
        self.lcd.message2(RadioMenu.MAIN_TITLE, "Starting up...")

    def loop(self):
        '''Main application loop. Receives input and dispatches one of either "up", "down", "select" or "back" commands.'''

        # display initial menu
        self.update(self.current_menu)

        while True:
            pass

    def update(self, menu):

        # show the "home" screen
        if not self.showing_menu:
            self.lcd.message2(RadioMenu.MAIN_TITLE, "Short press to start playing now or long press for menu")
            return

        # draw the current menu
        for (index, item) in enumerate(menu.items):
            if index == menu.selected_index:
                self.lcd.draw_menu(item.title, index, len(menu.items))

    def do_thing(self, item, arg):
        self.lcd.flash(str(time()), callback=self.close, interval=2)



