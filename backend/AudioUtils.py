import numpy as np

import display

def simple(rms):
    display.setStrip(display.secondary.value)
    display.setAmountColor(int(rms * display.LED_COUNT), display.primary.value)

def ruit(rms):
    rms = min(1, (3 * rms)**(2 + 1))
    display.setStrip(display.secondary.value)
    xmid = display.WIDTH / 2 - 0.5
    ymid = display.HEIGHT / 2 - 0.5
    i = int(rms * max(display.WIDTH, display.HEIGHT))
    for x in range(display.WIDTH):
        for y in range(display.HEIGHT):
            if abs(x - xmid) < i and abs(y - ymid) < i and abs(x - xmid) + abs(y - ymid) < i:
                display.setPixelColor(x, y, display.primary.value)
    display.strip.show()

from scipy.special import comb



def cirkel(rms):
    colorRGB = list(display.getRGBfromI(display.primary.value))
    licht = 0
    if rms > 0.5:
        if licht == 2:
            licht = 0
            for i in range(3):
                colorRGB[i] = 0
        else:
            licht += 1
    color = display.getIfromRGB(colorRGB)
    display.setStrip(display.secondary.value)
    xmid = display.WIDTH / 2 - 0.5
    ymid = display.HEIGHT / 2 - 0.5
    i = int(rms * max(display.WIDTH, display.HEIGHT))
    radius = rms*10
    for y in range(display.HEIGHT):
        for x in range(display.WIDTH):
            afstand = np.sqrt((y - ymid) ** 2 + (x - xmid) ** 2)
            if afstand < radius:
                display.setPixelColor(x, y, color)
    display.strip.show()

def sparkle(rms):
    rms = max(0, min(1, (3 * rms)**(2 + 1) - 0.1))
    display.setStrip(display.secondary.value)
    randoms = np.random.random((20, 18)) < rms
    for x, y in zip(*np.nonzero(randoms)):
        display.setPixelColor(x, y, display.primary.value)
    display.strip.show()

t = 0

def wave(rms):
    rms = rms = min(1, (3 * rms)**(2 + 1))
    display.setStrip(display.secondary.value)
    dt = 0.1
    global t
    t += dt
    xs = [4 * np.pi * x / (display.WIDTH - 1) for x in range(display.WIDTH)]
    color = display.primary.value
    ys = [int(rms * display.HEIGHT//2 * np.sin(x + t) + display.HEIGHT//2) for x in xs]
    display.setStrip(display.secondary.value)
    for x, y in zip(range(display.WIDTH), ys):
        display.setPixelColor(x, y, color)
        display.setPixelColor(x, y - 1, color)
        display.setPixelColor(x, y + 1, color)
    display.strip.show()

