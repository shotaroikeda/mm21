#! /usr/bin/env python2

from vis import visualizer as visual
from load_json import load_map_from_file as loadJson

# get Json file
with open('file') as json_file:
    JSobj = loadJson(json_file)

# Initalize Visualizer
a = visual.Visualizer(JSobj)
