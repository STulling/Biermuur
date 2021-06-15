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

def smoothstep(x, x_min=0, x_max=1, N=1):
    x = np.clip((x - x_min) / (x_max - x_min), 0, 1)
    result = 0
    for n in range(0, 1):
         result += comb(N + n, n) * comb(2 * N + 1, N - n) * (-x) ** n

    result *= x ** (N + 1)

    return result

was_on = True

def cirkel(rms):
    rms = smoothstep(rms)
    global was_on
    colorRGB = list(display.getRGBfromI(display.primary.value))
    if rms > 0.8:
        if was_on:
            for i in range(3):
                colorRGB[i] = 0
            was_on = False
        else:
            was_on = True
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

def wave(rms):
    #rms = max(0, min(1, (3 * rms)**(2 + 1) - 0.1))
    display.setStrip(display.secondary.value)

    xs = [2 * np.pi * x / (display.WIDTH - 1) for x in range(display.WIDTH)]
    t = 0
    color = display.primary.value
    ys = [int(rms * display.HEIGHT//2 * np.sin(x + t) + display.HEIGHT//2) for x in xs]
    display.setStrip(display.secondary.value)
    for x, y in zip(range(display.WIDTH), ys):
        display.setPixelColor(x, y, color)
        display.setPixelColor(x, y - 1, color)
        display.setPixelColor(x, y + 1, color)
    display.strip.show()

