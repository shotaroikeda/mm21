#! /usr/bin/env python2
from vis import visualizer as vis
from vis import vis_constants as const
from load_json import load_map_from_file as loadJson
import argparse

# Define arguements
parser = argparse.ArgumentParser(
    description="Lauches the visualizer")
parser.add_argument(
    "-x", "--width",
    help="Specifies the width of the visualizer",
    default=const.screenWidth,
    type=int)
parser.add_argument(
    "-y", "--height",
    help="Specifies the height of the visualizer",
    default=const.screenHeight,
    type=int)
parser.add_argument(
    "-m", "--mapJson",
    help="The map file for the visualizer",
    default="gamerunner/map.json")
args = parser.parse_args()  # parse args

try:
    with open(args.mapJson) as json_file:
        mapJsonObject = loadJson(json_file)
    if(mapJsonObject is None):
        raise Exception()
except IOError:
    print("File " + args.mapJson + " does not exist")
    raise
    exit(1)
except Exception:
    print("Failed to parse json data")
    raise
    exit(1)

# Initalize Visualizer
visualizer = vis.Visualizer(mapJsonObject, args.width, args.height)
