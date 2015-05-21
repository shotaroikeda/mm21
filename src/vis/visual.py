#!/usr/bin/env python2

import pygame2 as pg
import sys
import json
import time
import math
from visConstant import visConst as const
sys.path.insert(0, '../')
from load_json import load_map_from_file as loadJson

class visual(object):
    def __init__(self):
        self.screenHeight = const [ 'screenHeight' ]
        self.screenWidth = const[ 'screenWidth' ]
        self.title = const[ 'title' ]
        self.fps = const[ 'FPStgt' ]
        self.running = True
        pg.init()
        self.setup()

    def setup(self):
        pg.display.set_caption(self.title)
        pg.display.set_mode(self.screenHeight, self.screenWidth)
        self.gameClock = pg.time.Clock()

    def runFile(self, filename):
        with open(filename) as fp:
            self.JSfile = json.load(fp)

    def draw(self, args):
# Draw things

    def processAndDraw(self):
#do some stuff
