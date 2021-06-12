import numpy as np

import display

def simple(rms):
    display.setStrip(display.secondary, False)
    display.setAmountColor(int(rms * display.LED_COUNT), display.getIfromRGB(display.primary))

def ruit(rms):
    rms = min(1, (3 * rms)**(2 + 1))
    display.setStrip(display.secondary, False)
    xmid = display.WIDTH / 2 - 0.5
    ymid = display.HEIGHT / 2 - 0.5
    i = int(rms * max(display.WIDTH, display.HEIGHT))
    for x in range(display.WIDTH):
        for y in range(display.HEIGHT):
            if abs(x - xmid) < i and abs(y - ymid) < i and abs(x - xmid) + abs(y - ymid) < i:
                display.setPixelColor(x, y, display.getIfromRGB(display.primary))
    display.strip.show()


def sparkle(rms):
    rms = max(0, min(1, (3 * rms)**(2 + 1) - 0.1))
    display.setStrip(display.secondary, False)
    randoms = np.random.random((20, 18)) < rms
    for x, y in zip(*np.nonzero(randoms)):
        display.setPixelColor(x, y, display.getIfromRGB(display.primary))
    display.strip.show()