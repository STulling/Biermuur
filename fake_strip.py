from PIL import Image
import math
import os

NUM_PIXELS = 150
WIDTH = 12
HEIGHT = 12


class Adafruit_NeoPixel():
    im = Image.new('RGB', (12, 12))
    count = 0

    def __init__(self, LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL):
        super().__init__()

    def begin(self):
        return

    def setPixelColor(self, index, color):
        if 0 > index or index >= (WIDTH * HEIGHT):
            return
        y = math.floor(index / WIDTH)
        x = (WIDTH - 1 - (index - y * WIDTH) if y % 2 == 1 else index - y * WIDTH)
        self.im.putpixel((x, y), color)

    def numPixels(self):
        return NUM_PIXELS

    def show(self):
        if os.path.exists('image'):
            self.im.save(f'images/{self.count:05}.png')
            self.count += 1
