import time
from rpi_ws281x import *
import argparse
from PIL import Image, ImageDraw, ImageFont
import sys

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
        # out.show()
        time.sleep(speed)


def init():
    global strip
    # Create NeoPixel object with appropriate configuration.
    strip = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL)
    # Intialize the library (must be called once before other functions).
    strip.begin()
