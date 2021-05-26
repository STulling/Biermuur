import time

try:
    from rpi_ws281x import *
except ImportError:
    print("Missing rpi_ws281x library, running webserver anyway")
import argparse
from PIL import Image, ImageDraw, ImageFont
import sys
import numpy as np
import random
from fake_strip import FakeStrip

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
strip = FakeStrip()

fnt = ImageFont.truetype("Pixel12x10Mono.ttf", 13)
out = Image.new("RGB", (WIDTH, HEIGHT), (0, 255, 0))

primary = (0, 255, 0)
secondary = (255, 0, 0)


def getHTMLColors():
    return RGBToHTMLColor(primary), RGBToHTMLColor(secondary)


def RGBToHTMLColor(rgb_tuple):
    """ convert an (R, G, B) tuple to #RRGGBB """
    hexcolor = '#%02x%02x%02x' % rgb_tuple
    # that's it! '%02x' means zero-padded, 2-digit hex values
    return hexcolor


def HTMLColorToRGB(colorstring):
    """ convert #RRGGBB to an (R, G, B) tuple """
    colorstring = colorstring.strip()
    if colorstring[0] == '#': colorstring = colorstring[1:]
    r, g, b = colorstring[:2], colorstring[2:4], colorstring[4:]
    r, g, b = [int(n, 16) for n in (r, g, b)]
    return r, g, b


def setTheme(HTMLPrimary, HTMLSecondary):
    global primary
    global secondary
    primary = HTMLColorToRGB(HTMLPrimary)
    secondary = HTMLColorToRGB(HTMLSecondary)


def setPixelColor(x, y, color):
    if x < 0 or y < 0:
        return
    if x >= WIDTH or y >= HEIGHT:
        return
    if y % 2 == 1:
        x = 11 - x
    loc = x + y * WIDTH
    strip.setPixelColor(loc, color)


def setStrip(color, update=True):
    for i in range(LED_COUNT):
        strip.setPixelColor(i, getIfromRGB(color))
    if update:
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


def movingText(text, speed, loop=False):
    moving_width = 10 * 2 + 10 * len(text)
    d = ImageDraw.Draw(out)
    d.fontmode = "1"
    while True:
        for x in range(moving_width):
            wipeImage(out, secondary)
            d.multiline_text((10 - x, 1), text, font=fnt, fill=primary)
            show(out)
            time.sleep(speed)
        if not loop:
            break


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
    while True:
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

def diamondwipe(color=(255, 255, 0)):
    xmid = WIDTH // 2
    ymid = HEIGHT // 2
    for i in range(max(WIDTH, HEIGHT)):
        for x, y in list(enumerate(reversed(range(i)))):
            coords = [(xmid + x, ymid + y), (xmid - 1 - x, ymid + y), (xmid + x, ymid - 1 - y),
                      (xmid - 1 - x, ymid - 1 - y)]
            for x, y in coords:
                if 0 <= x < WIDTH and 0 <= y < HEIGHT:
                    setPixelColor(x, y, getIfromRGB(color))
        strip.show()
        time.sleep(1 / 20.0)

def diamond_wipes():
    while True:
        r = random.randint(0, 1) * 255
        g = random.randint(0, 1) * 255
        b = random.randint(0, 1) * 255
        color = (r, g, b)
        diamondwipe(color=color)

def random_pixel():
    indices = list(range(WIDTH * HEIGHT))
    while True:
        random.shuffle(indices)
        for pixel in indices:
            color = random.randint(0, 16777215)
            strip.setPixelColor(pixel, color)
            strip.show()
            time.sleep(1 / 20.0)

def random_order_wipe():
    indices = list(range(WIDTH * HEIGHT))
    while True:
        random.shuffle(indices)
        color = random.randint(0, 16777215)
        for pixel in indices:
            strip.setPixelColor(pixel, color)
            strip.show()
            time.sleep(1 / 20.0)

def init():
    global strip
    # Create NeoPixel object with appropriate configuration.
    strip = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL)
    # Intialize the library (must be called once before other functions).
    strip.begin()


def randomwoord():
    p = ['MAAK PUZZEL', 'EIGEN KWEEK TIJD', 'KAMP HELAAS', 'SLA KWEKEN', 'KUNSTGRAS']
    x = random.choice(p)
    movingText(x, 0.04)


def golf():
    xs = [2 * np.pi * x / 11 for x in range(12)]
    t = 0
    dt = 0.025
    color = Color(0, 255, 255)
    while True:
        t += dt
        ys1 = [int(6 * np.sin(x + t) + 6) for x in xs]
        ys2 = [int(6 * np.sin(x + t + np.pi) + 6) for x in xs]
        setStrip((0, 0, 255), False)
        for x, y in zip(range(12), ys1):
            setPixelColor(x, y, color)
            setPixelColor(x, y-1, color)
            setPixelColor(x, y+1, color)
        for x, y in zip(range(12), ys2):
            setPixelColor(x, y, color)
            setPixelColor(x, y-1, color)
            setPixelColor(x, y+1, color)
        strip.show()
        time.sleep(0.01)

def lijnen():
    hoeken = np.linspace(-2, 2, 20)
    while True:
        alpha = random.choice(hoeken)
        yas = 6
        y = []
        x = [0,1,2,3,4,5,6,7,8,9,10,11]
        for i in x:
            yval = alpha * i + yas
            while yval > 0 and yval<12:
               np.append(y, yval)
        setStrip((0, 0, 255), False)
        color = Color(0, 255, 255)
        for x, y in zip(range(y), y):
            setPixelColor(x, y, color)
        strip.show()
        time.sleep(0.05)

