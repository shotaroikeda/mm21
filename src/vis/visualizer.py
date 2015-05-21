#!/usr/bin/env python2
import pygame as pg
import sys
import json
import time
import math
sys.path.insert(0, '../')
from load_json import load_map_from_file as loadJson
import vis_constants as const


class Visualizer(object):

    def __init__(self):
        self.screenHeight = const.screenHeight
        self.screenWidth = const.screenWidth
        self.title = const.title
        self.fps = const.FPStgt
        self.running = True
        pg.init()
        self.setup()

    def setup(self):
        pg.display.set_caption(self.title)
        pg.display.set_mode(self.screenHeight, self.screenWidth)
        self.gameClock = pg.time.Clock()

    def runFile(self, filename):
        with open(filename) as json_file:
            self.JSfile = json.load(json_file)

    def draw(self, args):
# Draw things

    def processAndDraw(self):
#do some stuff

# Just for now
if __name__ == "__main__":
    vis = Visualizer()
