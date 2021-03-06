import time
import sys
from multiprocessing import Value

try:
    from rpi_ws281x import *
except ImportError:
    print("Missing rpi_ws281x library, using simulated strip")
    if 'fake_strip' not in sys.modules:
        from fake_strip import *
import argparse
from PIL import Image, ImageDraw, ImageFont
import numpy as np
import random

# LED strip configuration:
LED_COUNT = 360  # Number of LED pixels.
LED_PIN = 21  # GPIO pin connected to the pixels (18 uses PWM!).
LED_FREQ_HZ = 800000  # LED signal frequency in hertz (usually 800khz)
LED_DMA = 10  # DMA channel to use for generating signal (try 10)
LED_BRIGHTNESS = 255  # Set to 0 for darkest and 255 for brightest
LED_INVERT = False  # True to invert the signal (when using NPN transistor level shift)
LED_CHANNEL = 0  # set to '1' for GPIOs 13, 19, 41, 45 or 53
WIDTH = 20
HEIGHT = 18
KRAT_WIDTH = 4
KRAT_HEIGHT = 6
N_KRAT_X = 5
N_KRAT_Y = 3

fnt = ImageFont.truetype("Pixel12x10Mono.ttf", 13)
out = Image.new("RGB", (WIDTH, HEIGHT), (0, 255, 0))

primary = Value('i', Color(0, 0, 255))
secondary = Value('i', Color(0, 0, 0))
strip = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL)


def setAmountColor(n, color):
    for i in range(min(n, LED_COUNT)):
        strip.setPixelColor(i, color)
    strip.show()

def setPixelColor(x, y, color):
    if x < 0 or y < 0:
        return
    if x >= WIDTH or y >= HEIGHT:
        return
    if y % 2 == 1:
        x = WIDTH - 1 - x
    loc = int(x + y * WIDTH)
    strip.setPixelColor(loc, color)


# TODO: Fix
def getHTMLColors():
    return RGBToHTMLColor(primary.value), RGBToHTMLColor(secondary.value)

def getRGBfromI(RGBint):
    blue = RGBint & 255
    green = (RGBint >> 8) & 255
    red = (RGBint >> 16) & 255
    return red, green, blue

def RGBToHTMLColor(rgb_tuple):
    """ convert an (R, G, B) tuple to #RRGGBB """
    newrgb = (rgb_tuple[1], rgb_tuple[0], rgb_tuple[2])
    hexcolor = '#%02x%02x%02x' % newrgb
    # that's it! '%02x' means zero-padded, 2-digit hex values
    return hexcolor


def HTMLColorToRGB(colorstring):
    """ convert #RRGGBB to an (R, G, B) tuple """
    colorstring = colorstring.strip()
    if colorstring[0] == '#': colorstring = colorstring[1:]
    r, g, b = colorstring[:2], colorstring[2:4], colorstring[4:]
    r, g, b = [int(n, 16) for n in (r, g, b)]
    return g, r, b


def setTheme(HTMLPrimary, HTMLSecondary):
    global primary
    global secondary
    primary.value = getIfromRGB(HTMLColorToRGB(HTMLPrimary))
    secondary.value = getIfromRGB(HTMLColorToRGB(HTMLSecondary))

def clear():
    setStrip(0)
    strip.show()

def setStrip(color):
    for i in range(LED_COUNT):
        strip.setPixelColor(i, color)

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


def display(arr):
    for y in range(len(arr)):
        for x in range(len(arr[y])):
            setPixelColor(x, y, Color(arr[y][x][0], arr[y][x][1], arr[y][x][2]))
    strip.show()


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
                setPixelColor(x, y, getIfromRGB(color))
        strip.show()
        time.sleep(1 / 20.0)


def diamond_wipes():
    color = (0, 0, 0)
    last_color = color
    while True:
        while color is last_color:
            r = random.randint(0, 1) * 255
            g = random.randint(0, 1) * 255
            b = random.randint(0, 1) * 255
            color = (r, g, b)
        diamondwipe(color=color)
        last_color = color


def random_pixel():
    NUM_PIXELS = WIDTH * HEIGHT
    indices = list(range(NUM_PIXELS))
    while True:
        random.shuffle(indices)
        for pixel in indices:
            color = random.randint(0, 16777215)
            strip.setPixelColor(pixel, color)
            strip.show()
            time.sleep(1 / NUM_PIXELS)


def random_order_wipe():
    NUM_PIXELS = WIDTH * HEIGHT
    indices = list(range(NUM_PIXELS))
    while True:
        random.shuffle(indices)
        color = random.randint(0, 16777215)
        for pixel in indices:
            strip.setPixelColor(pixel, color)
            strip.show()
            time.sleep(1 / NUM_PIXELS)


def init():
    # Create NeoPixel object with appropriate configuration.
    # Intialize the library (must be called once before other functions).
    strip.begin()


def randomwoord():
    p = ['NIET ZEUREN FEUT', 'TWEE GROENE JONGENS', 'GEEN SPOILERS!', 'BRO NEEM WAT SLA',
         'VOOR OF NA 1 UUR', 'DAAR ZIT POTENTIE IN', 'IK BEN EEN WETENSCHAPPER BTW',
         'MEER KRATTEN']
    x = random.choice(p)
    movingText(x, 0.04)

def dobbelsteen():
    for i in range(30):
        setStrip(secondary.value)
        p = [1,2,3,4,5,6]
        kleuren = [Color(255,0,0),
                   Color(0,255,0),
                   Color(0,0,255),
                   Color(255,0,255),
                   Color(255,255,0),
                   Color(0,255,255)]
        ogen = random.choice(p)
        kleur = kleuren[ogen]
        xval = np.arange(0, KRAT_WIDTH, 1)
        yval = np.arange(0, KRAT_HEIGHT, 1)
        if ogen == 2 or ogen == 3 or ogen == 4 or ogen == 5 or ogen ==6:
            xval1 = xval + 1*KRAT_WIDTH
            yval1 =  yval + 0*KRAT_HEIGHT
            for y in yval1:
                for x in xval1:
                    setPixelColor(x, y, kleur)
        if ogen == 2 or ogen == 3 or ogen == 4 or ogen == 5 or ogen ==6:
            xval2 = xval + 3 * KRAT_WIDTH
            yval2 = yval + 2 * KRAT_HEIGHT
            for y in yval2:
                for x in xval2:
                    setPixelColor(x, y, kleur)
        if ogen == 3  or ogen == 5 or ogen == 1:
            xval3 = xval +  2 * KRAT_WIDTH
            yval3 =  yval + 1* KRAT_HEIGHT
            for y in yval3:
                for x in xval3:
                    setPixelColor(x, y, kleur)
        if  ogen == 4 or ogen == 5 or ogen ==6:
            xval4 = xval + 1 * KRAT_WIDTH
            yval4 = yval + 2 * KRAT_HEIGHT
            for y in yval4:
                for x in xval4:
                    setPixelColor(x, y, kleur)
        if ogen == 4 or ogen == 5 or ogen == 6:
            xval5 = xval + 3 * KRAT_WIDTH
            yval5 = yval + 0 * KRAT_HEIGHT
            for y in yval5:
                for x in xval5:
                    setPixelColor(x, y, kleur)
        if ogen == 6:
            xval8 = xval + 1 * KRAT_WIDTH
            yval8 = yval + 1 * KRAT_HEIGHT
            for y in yval8:
                for x in xval8:
                    setPixelColor(x, y, kleur)
            xval9 = xval + 3 * KRAT_WIDTH
            yval9 = yval + 1 * KRAT_HEIGHT
            for y in yval9:
                for x in xval9:
                    setPixelColor(x, y, kleur)
        strip.show()
        time.sleep(0.1)
def golf():
    xs = [2 * np.pi * x / 11 for x in range(12)]
    t = 0
    dt = 0.025
    color = getIfromRGB(primary)
    while True:
        t += dt
        ys1 = [int(6 * np.sin(x + t) + 6) for x in xs]
        ys2 = [int(6 * np.sin(x + t + np.pi) + 6) for x in xs]
        setStrip(secondary.value)
        for x, y in zip(range(12), ys1):
            setPixelColor(x, y, color)
            setPixelColor(x, y - 1, color)
            setPixelColor(x, y + 1, color)
        for x, y in zip(range(12), ys2):
            setPixelColor(x, y, color)
            setPixelColor(x, y - 1, color)
            setPixelColor(x, y + 1, color)
        strip.show()
        time.sleep(0.01)


def lijnen():
    hoeken = np.linspace(-2, 2, 10)
    while True:
        setStrip(secondary.value)
        alpha = random.choice(hoeken)
        xcenter = random.randint(0, WIDTH)
        ycenter = random.randint(0, HEIGHT)
        yas = ycenter - (xcenter * alpha)
        for x in range(WIDTH):
            yval = int(alpha * x + yas)
            setPixelColor(x, yval, primary.value)
            strip.show()
            time.sleep(0.02)
        strip.show()
        # time.sleep(0.2)



def cirkels():
    while True:
        color = random.randint(0, 16777215)
        xcenter = random.randint(3, 9)
        ycenter = random.randint(3, 9)
        straalmax = 1
        for straal in range(12):
            for y in range(HEIGHT):
                for x in range(WIDTH):
                    afstand = np.sqrt((y - ycenter) ** 2 + (x - xcenter) ** 2)
                    if afstand < straal:
                        setPixelColor(x, y, color)
            strip.show()
            time.sleep(0.1)
        setStrip(secondary.value)


def cirkel(radius):
    color = random.randint(0, 16777215)
    xcenter = random.randint(3, 9)
    ycenter = random.randint(3, 9)
    for y in range(HEIGHT):
        for x in range(WIDTH):
            afstand = np.sqrt((y - ycenter) ** 2 + (x - xcenter) ** 2)
            if afstand < radius:
                setPixelColor(x, y, color)
    strip.show()
    time.sleep(0.1)
    setStrip(secondary.value)


def histogram():
    while True:
        x = range(12)
        for i in x:
            y = random.randint(0, 11)
            color = random.randint(0, 16777215)
            for yval in range(y):
                setPixelColor(i, 11 - yval, color)
            strip.show()
        time.sleep(0.05)
        setStrip(secondary.value)


def matrix():
    zero = [(-1, -3),
            (0, -3),
            (1, -3),
            (-1, -2),
            (1, -2),
            (-1, -1),
            (1, -1),
            (-1, 0),
            (0, 0),
            (1, 0)]
    one = [(-1, -3),
           (0, -3),
           (0, -2),
           (0, -1),
           (-1, 0),
           (0, 0),
           (1, 0)]
    zeros = [(random.randint(-2, WIDTH + 2), -3),
             (random.randint(-2, WIDTH + 2), -7),
             (random.randint(-2, WIDTH + 2), -9)]
    ones = [(random.randint(-2, WIDTH + 2), -1),
            (random.randint(-2, WIDTH + 2), -6),
            (random.randint(-2, WIDTH + 2), -11)]
    while True:
        setStrip(secondary.value)
        for i, (x, y) in enumerate(zeros):
            if y > HEIGHT + 4:
                zeros[i] = (random.randint(-2, WIDTH + 2), -3)
            else:
                zeros[i] = (x, y + 1)
            for xoff, yoff in zero:
                setPixelColor(x + xoff, y + yoff, primary.value)
        for i, (x, y) in enumerate(ones):
            if y > HEIGHT + 4:
                ones[i] = (random.randint(-2, WIDTH + 2), -3)
            else:
                ones[i] = (x, y + 1)
            for xoff, yoff in one:
                setPixelColor(x + xoff, y + yoff, primary.value)
        strip.show()
        time.sleep(0.1)


def spiraal():
    while True:
        r = 1
        theta = 2 * np.pi
        setStrip(secondary.value)
        while r < 15:
            theta += 0.05 * np.pi
            r += 0.01
            x = int(r * np.cos(theta)) + (WIDTH // 2)
            y = int(r * np.sin(theta)) + (HEIGHT // 2)
            print(x, y)
            setPixelColor(x, y, primary.value)
            strip.show()
            time.sleep(0.05)


def boxes():
    while True:
        setStrip(secondary.value)
        xval = np.arange(0, KRAT_WIDTH, 1)
        yval = np.arange(0, KRAT_HEIGHT, 1)
        kratx = random.randint(0, N_KRAT_X-1)
        kraty = random.randint(0, N_KRAT_Y-1)
        xval += kratx * KRAT_WIDTH
        yval += kraty * KRAT_HEIGHT
        for y in yval:
            for x in xval:
                setPixelColor(x, y, primary.value)
        strip.show()
        time.sleep(0.05)



