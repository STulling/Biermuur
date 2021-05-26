from PIL import Image
import math

NUM_PIXELS = 150
WIDTH = 12
HEIGHT = 12


class FakeStrip():
    im = Image.new('RGB', (12, 12))
    count = 0

    def __init__(self):
        super().__init__()

    def setPixelColor(self, index, color):
        if 0 > index or index >= (WIDTH * HEIGHT):
            return
        y = math.floor(index / WIDTH)
        x = (WIDTH - 1 - (index - y * WIDTH) if y % 2 == 1 else index - y * WIDTH)
        self.im.putpixel((x, y), color)

    def numPixels(self):
        return NUM_PIXELS

    def show(self):
        self.im.save(f'images/{self.count:05}.png')
        self.count += 1
