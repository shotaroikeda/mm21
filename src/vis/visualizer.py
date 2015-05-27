#!/usr/bin/env python2
import pygame as pg
import sys
import json
import time
import math
import vis_constants as const


class Visualizer(object):

    def __init__(self, jsFile):
        self.screenHeight = const.screenHeight
        self.screenWidth = const.screenWidth
        self.title = const.title
        self.fps = const.FPStgt
        self.JSfile = jsFile
        self.running = True
        pg.init()
        self.setup()

    def setup(self):
        pg.display.set_caption(self.title)
        pg.display.set_mode((self.screenHeight, self.screenWidth))
        self.gameClock = pg.time.Clock()
    def draw(self, args):
        print ""
# Draw things
    def processAndDraw(self):
        print ""
#do some stuff

# Just for now
if __name__ == "__main__":
    vis = Visualizer(2)
