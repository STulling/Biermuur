import numpy as np
import random
import display
import time

def simple(rms):
    display.setStrip(display.secondary.value)
    display.setAmountColor(int(rms * display.LED_COUNT), display.primary.value)

def ruit(rms):
    display.setStrip(display.secondary.value)
    xmid = display.WIDTH / 2 - 0.5
    ymid = display.HEIGHT / 2 - 0.5
    i = int(rms * max(display.WIDTH, display.HEIGHT))
    for x in range(display.WIDTH):
        for y in range(display.HEIGHT):
            if abs(x - xmid) < i and abs(y - ymid) < i and abs(x - xmid) + abs(y - ymid) < i:
                display.setPixelColor(x, y, display.primary.value)
    display.strip.show()

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
    display.setStrip(display.secondary.value)
    for x in range(display.WIDTH):
        for y in range(display.HEIGHT):
            if random.random() < rms:
                display.setPixelColor(x, y, display.primary.value)
    display.strip.show()

t = 0

def wave(rms):
    display.setStrip(display.secondary.value)
    dt = 0.1
    global t
    t += dt
    xs = [3 * np.pi * x / (display.WIDTH - 1) for x in range(display.WIDTH)]
    color = display.primary.value
    ys = [int(rms * display.HEIGHT//2 * np.sin(x + t) + display.HEIGHT//2) for x in xs]
    display.setStrip(display.secondary.value)
    for x, y in zip(range(display.WIDTH), ys):
        display.setPixelColor(x, y, color)
        display.setPixelColor(x, y - 1, color)
    display.strip.show()


def mond(rms):
    display.setStrip(display.secondary.value)
    h = display.WIDTH/2
    k = display.HEIGHT/2
    a = display.WIDTH/2
    b = rms
    for x in range(display.WIDTH):
        y = np.sqrt((1 - ((x-h)**2/b**2))*a**2) + k
        display.setPixelColor(x, y, display.primary.value)
        display.setPixelColor(x, 2*k-y, display.primary.value)
    display.strip.show()

def bliksem(rms):
    hoeken = np.linspace(-2, 2, 10)
    alpha1 = random.choice(hoeken)
    alpha2 = random.choice(hoeken)
    alpha3 = random.choice(hoeken)
    #alpha4 = random.choice(hoeken)
    #alpha5 = random.choice(hoeken)
    display.setStrip(display.secondary.value)
    xstart = random.randint(6,display.WIDTH-6)

    xval1 = []
    yval1 = []
    xval2 = []
    yval2 = []

    if alpha1 < 0:
        xval1 = np.arange(-5,0) + xstart
    else:
        xval1 = np.arange(0,5) + xstart
    yval1 = xval1*alpha1
    if alpha2 < 0:
        xval2 = np.arange(-5,0) + xval1[3]
        print(xval2)
    else:
        xval1 = np.arange(0,5) + xval1[3]
    yval2 = xval1*alpha2 + yval1[3]
    if alpha3 < 0:
        xval3 = np.arange(-5,0) + xval2[3]
    else:
        xval3 = np.arange(0,5) + xval2[3]
    yval3 = xval3*alpha3 + yval2[3]
    for i in range(len(xval1)):
        display.setPixelColor(xval1[i], yval1[i], display.primary.value)
        display.setPixelColor(xval2[i], yval2[i], display.primary.value)
        display.setPixelColor(xval3[i], yval3[i], display.primary.value)
    display.strip.show()