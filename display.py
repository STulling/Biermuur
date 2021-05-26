import time

try:
    from rpi_ws281x import *
except ImportError:
    print("Missing rpi_ws281x library, running webserver anyway")
import argparse
from PIL import Image, ImageDraw, ImageFont
import sys
import random

# LED strip configuration:
LED_COUNT = 144  # Number of LED pixels.
LED_PIN = 18  # GPIO pin connected to the pixels (18 uses PWM!).
LED_FREQ_HZ = 800000  # LED signal frequency in hertz (usually 800khz)
LED_DMA = 10  # DMA channel to use for generating signal (try 10)
LED_BRIGHTNESS = 255  # Set to 0 for darkest and 255 for brightest
LED_INVERT = False  # True to invert the signal (when using NPN transistor level shift)
LED_CHANNEL = 0  # set to '1' for GPIOs 13, 19, 41, 45 or 53
WIDTH = 12
HEIGHT = 12
strip = None

fnt = ImageFont.truetype("Pixel12x10Mono.ttf", 13)
out = Image.new("RGB", (WIDTH, HEIGHT), (0, 255, 0))


def setPixelColor(x, y, color):
    if y % 2 == 1:
        x = 11 - x
    loc = x + y * WIDTH
    strip.setPixelColor(loc, color)


def setStrip(color):
    for i in range(LED_COUNT):
        strip.setPixelColor(i, getIfromRGB(color))
    strip.show()


def show(image):
    for x in range(WIDTH):
        for y in range(HEIGHT):
            setPixelColor(x, y, getIfromRGB(image.getpixel((x, y))))
    strip.show()


def wipeImage(image, color):
    for y in range(image.size[1]):
        for x in range(image.size[0]):
            image.putpixel((x, y), color)


def getIfromRGB(rgb):
    red = rgb[0]
    green = rgb[1]
    blue = rgb[2]
    RGBint = (red << 16) + (green << 8) + blue
    return RGBint


def movingText(text, speed):
    moving_width = 10 * 2 + 10 * len(text)
    d = ImageDraw.Draw(out)
    d.fontmode = "1"
    for x in range(moving_width):
        wipeImage(out, (255, 0, 0))
        d.multiline_text((10 - x, 1), text, font=fnt, fill=(0, 255, 0))
        show(out)
        time.sleep(speed)


def wheel(pos):
    """Generate rainbow colors across 0-255 positions."""
    if pos < 85:
        return Color(pos * 3, 255 - pos * 3, 0)
    elif pos < 170:
        pos -= 85
        return Color(255 - pos * 3, 0, pos * 3)
    else:
        pos -= 170
        return Color(0, pos * 3, 255 - pos * 3)


def rainbow(wait_ms=20, iterations=1):
    """Draw rainbow that fades across all pixels at once."""
    for j in range(256 * iterations):
        for i in range(strip.numPixels()):
            strip.setPixelColor(i, wheel((i + j) & 255))
        strip.show()
        time.sleep(wait_ms / 1000.0)


def rainbowCycle(wait_ms=20, iterations=5):
    """Draw rainbow that uniformly distributes itself across all pixels."""
    for j in range(256 * iterations):
        for i in range(strip.numPixels()):
            strip.setPixelColor(i, wheel((int(i * 256 / strip.numPixels()) + j) & 255))
        strip.show()
        time.sleep(wait_ms / 1000.0)


def theaterChaseRainbow(wait_ms=50):
    """Rainbow movie theater light style chaser animation."""
    for j in range(256):
        for q in range(3):
            for i in range(0, strip.numPixels(), 3):
                strip.setPixelColor(i + q, wheel((i + j) % 255))
            strip.show()
            time.sleep(wait_ms / 1000.0)
            for i in range(0, strip.numPixels(), 3):
                strip.setPixelColor(i + q, 0)


def shapewipe(shape=None, color=(255, 255, 0)):
    grow_size = max(WIDTH, HEIGHT)
    d = ImageDraw.Draw(out)
    for x in range(grow_size):
        wipeImage(out, (255, 0, 0))
        sizedshape = [(i[0] * x + WIDTH / 2, i[1] * x + HEIGHT / 2) for i in shape]
        d.polygon(xy=sizedshape, fill=color, outline=color)
        sizedshape = [(i[0] * x + WIDTH / 2 - 1, i[1] * x + HEIGHT / 2) for i in shape]
        d.polygon(xy=sizedshape, fill=color, outline=color)
        sizedshape = [(i[0] * x + WIDTH / 2, i[1] * x + HEIGHT / 2 - 1) for i in shape]
        d.polygon(xy=sizedshape, fill=color, outline=color)
        sizedshape = [(i[0] * x + WIDTH / 2 - 1, i[1] * x + HEIGHT / 2 - 1) for i in shape]
        d.polygon(xy=sizedshape, fill=color, outline=color)
        show(out)
        time.sleep(1/500)


def diamondwipe(color=(255, 255, 0)):
    star = [(0, -2), (2, 0), (0, 2), (-2, 0)]
    shapewipe(shape=star, color=color)


def diamondwipes(times=5):
    for i in range(times):
        r = random.randint(0, 1) * 255
        g = random.randint(0, 1) * 255
        b = random.randint(0, 1) * 255
        color = (r, g, b)
        diamondwipe(color=color)


def starwipe(color=(255, 255, 0)):
    star = [(0, -1), (0.588, 0.8), (-0.951, -0.309), (0.951, -0.309), (-0.588, 0.8)]
    shapewipe(shape=star, color=color)


def init():
    global strip
    # Create NeoPixel object with appropriate configuration.
    strip = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL)
    # Intialize the library (must be called once before other functions).
    strip.begin()
