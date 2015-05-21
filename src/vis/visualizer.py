#!/usr/bin/env python2

import pygame as pg
import sys
import json
import time
import math
<<<<<<< HEAD:src/vis/visual.py
from visConstant import visConst as const
sys.path.insert(0, '../')
from load_json import load_map_from_file as loadJson
=======
import vis_constants as const


class Visualizer(object):
>>>>>>> 92ca435047a4dbcce23aedb3a5c348e2ada61e57:src/vis/visualizer.py

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
<<<<<<< HEAD:src/vis/visual.py
        with open(filename) as fp:
            self.JSfile = json.load(fp)

    def draw(self, args):
# Draw things

    def processAndDraw(self):
#do some stuff
=======
        try:
            with open(filename) as json_file:
                print "GG EASY"
        except:
            print "We fucked up " + filename + "! JK, the file doesn't exist!"
            sys.exit(69)


# Just for now
vis = Visualizer()
>>>>>>> 92ca435047a4dbcce23aedb3a5c348e2ada61e57:src/vis/visualizer.py
