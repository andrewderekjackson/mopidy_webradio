from time import sleep
import Image, ImageFont, ImageDraw, os

import Adafruit_ILI9341 as TFT
import Adafruit_GPIO as GPIO
import Adafruit_GPIO.SPI as SPI

# TFT configuration
DC = 18
RST = 23
SPI_PORT = 0
SPI_DEVICE = 0

X_MAX = 320
Y_MAX = 240
MARGIN = 5

class LcdController(object):

    def __init__(self):
        self.disp = TFT.ILI9341(DC, rst=RST, spi=SPI.SpiDev(SPI_PORT, SPI_DEVICE, max_speed_hz=64000000))

        # Initialize display.
        self.disp.begin()
        self.font_dir = os.path.dirname(os.path.realpath(__file__)) + "/fonts"
        self._last_image = None

    def now_playing(self, cover_image, primary_text, secondary_text):

        image = self._create_now_playing(cover_image, primary_text, secondary_text)

        self._last_image = image
        self.disp.display(image.rotate(90))

    def message(self, message_string):

        image = Image.new("RGB", (X_MAX, Y_MAX), "white")
        font = ImageFont.load(self.font_dir + "/courB12.pil")

        draw = ImageDraw.Draw(image)

        w, h = draw.textsize(message_string, font=font)

        draw.text(((X_MAX-w)/2,(Y_MAX-h)/2),
                  message_string,
                  font=font,
                  fill='black')

        self.disp.display(image.rotate(90))

    def show_last_screen(self):
        if self._last_image is not None:
            self.disp.display(self._last_image.rotate(90))

    def _create_now_playing(self, image_file, artist_text, title_text):

        cover = Image.open(image_file)
        cover.thumbnail((X_MAX-50, Y_MAX-50))

        image = Image.new("RGB", (X_MAX, Y_MAX), "white")
        image.paste(cover, (X_MAX/2 - cover.size[0]/2, MARGIN))



        font = ImageFont.load(self.font_dir + "/courB12.pil")
        font_bold = ImageFont.load(self.font_dir + "/courB12.pil")

        draw = ImageDraw.Draw(image)

        title_text_size = font.getsize(title_text)
        draw.text((X_MAX/2-title_text_size[0]/2, Y_MAX-title_text_size[1] - MARGIN),
                  title_text,
                  font=font,
                  fill='black')

        artist_text_size = font_bold.getsize(artist_text)
        draw.text((X_MAX/2-artist_text_size[0]/2, Y_MAX-artist_text_size[1] - 17 - MARGIN),
                  artist_text,
                  font=font_bold,
                  fill='black')

        return image





