from PIL import Image
import math
import pygame
import os
import display
import threading
import time

def Color(r, g, b):
    RGBint = (r << 16) + (g << 8) + b
    return RGBint


def getRGBfromI(RGBint):
    blue = RGBint & 255
    green = (RGBint >> 8) & 255
    red = (RGBint >> 16) & 255
    return red, green, blue


class Adafruit_NeoPixel():
    count = 0

    def __init__(self, LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL):
        self.NUM_PIXELS = LED_COUNT
        self.WIDTH = display.WIDTH
        self.HEIGHT = display.HEIGHT
        self.SCREEN = None

    def begin(self):
        pygame.init()
        self.SCREEN = pygame.display.set_mode((self.WIDTH * 20, self.HEIGHT * 20))
        self.SCREEN.fill((0, 0, 0))
        return

    def setPixelColor(self, index, color):
        if 0 > index or index >= (self.WIDTH * self.HEIGHT):
            return
        y = math.floor(index / self.WIDTH)
        x = (self.WIDTH - 1 - (index - y * self.WIDTH) if y % 2 == 1 else index - y * self.WIDTH)
        self.drawRect(x, y, getRGBfromI(color))

    def drawRect(self, x, y, color):
        rect = pygame.Rect(x*20 + 1, y*20 + 1, 19, 19)
        pygame.draw.rect(self.SCREEN, color, rect)

    def numPixels(self):
        return self.NUM_PIXELS

    def show(self):
        pygame.display.update()
