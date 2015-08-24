#! /usr/bin/env python2
from vis import visualizer as vis
from vis import vis_constants as const
from load_json import load_map_from_file as loadJson
import json
import argparse

# Define arguements
parser = argparse.ArgumentParser(
    description="Launches the visualizer")
parser.add_argument(
    "-f", "--logFile",
    help="Specifies a log file to use",
    default=None)
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
parser.add_argument("-d", "--debug", help="Turn on Debug", dest='debug', action='store_true')
parser.add_argument("-s", "--scoreboard", help="Turn on Scoreboard", dest='scoreboard', action='store_true')
parser.set_defaults(debug=False)
args = parser.parse_args()  # parse args

try:
    with open(args.mapJson) as json_file:
        mapJsonObject = loadJson(json_file)
    if(mapJsonObject is None):
        raise Exception
except IOError:
    print("File " + args.mapJson + " does not exist")
    raise
    exit(1)
except Exception:
    print("Failed to parse map json data")
    raise
    exit(1)

if (args.logFile is not None):
    try:
        with open(args.logFile) as json_file:
            logJsonObject = json.load(json_file)
        if(logJsonObject is None):
            raise Exception
    except IOError:
        print("File " + args.logJson + " does not exist")
        raise
        exit(1)
    except Exception:
        print("Failed to parse log json data")
        raise
        exit(1)

# Initialize Visualizer
if (args.logFile is not None):
    visualizer = vis.Visualizer(mapJsonObject, args.width, args.height, args.debug, args.scoreboard, logJsonObject)
else:
    visualizer = vis.Visualizer(mapJsonObject, args.width, args.height, args.debug, args.scoreboard)
