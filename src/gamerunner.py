#!/usr/bin/env python2
import os
import sys
import os.path as op
path = op.dirname(op.dirname(op.realpath(__file__)))
print path
sys.path.append(path)
from server.server import MMServer
from subprocess import Popen
import argparse
from objects import game
# import pickle
from vis.visualizer import Visualizer
from vis.scoreboard import Scoreboard
import threading
from load_json import load_map_from_file as loadJson
import json
# from urllib2 import urlopen, URLError
# import time
# from functools import partial

import misc_constants as miscConstants
import game_constants as gameConstants

FNULL = open(os.devnull, 'w')

parameters = None
client_list = list()


def launch_clients():
    if parameters.client:
        numberOfClients = len(parameters.client)
        for client in parameters.client:
            launch_client(os.path.join(os.path.dirname(os.path.realpath(__file__)), os.pardir, 'test-clients/', client))
    else:
        numberOfClients = 0
    for x in xrange(numberOfClients, parameters.teams):
        launch_client(os.path.join(os.getcwd(), parameters.defaultClient))


def launch_client(client, port=None):
    c = Client_program(client, port)
    client_list.append(c)
    c.run()


def launch_client_test_game(client, port):
    launch_client(os.path.join(os.path.dirname(os.path.realpath(__file__)), os.pardir, client), port)
    launch_client(os.path.join(os.getcwd(), parameters.defaultClient), port)


def parse_args():
    parser = argparse.ArgumentParser(
        description="Launch the server with p clients which "
        + "connect to it.")
    parser.add_argument(
        "-u", "--port",
        help="Specify the port the server runs on. " +
        "Default: {0}".format(miscConstants.port),
        default=miscConstants.port,
        type=int)
    parser.add_argument(
        "-w", "--debug-view",
        help="Run the debug view.",
        const=True,
        default=False,
        action="store_const",
    )
    parser.add_argument(
        "-m", "--map",
        help="Specify the map file the game should use. " +
        "Default: {0}".format(miscConstants.mapFile),
        default=miscConstants.mapFile)
    """
    parser.add_argument(
        "-o", "--mapBackground",
        help="Specify map image to show the game on. " +
        "Default: {0}".format(miscConstants.mapBackground),
        default=miscConstants.mapBackground)
    """
    parser.add_argument(
        "-l", "--log",
        help="Specify where the game log will be written to. " +
        "For example, ./gamerunner.py --log LOG.out. Default: {0}".
        format(miscConstants.logFile),
        default=miscConstants.logFile)
    parser.add_argument(
        "-t", "--teams",
        help="Specifies the number of teams. Default: {0}."
        .format(gameConstants.numPlayers),
        default=gameConstants.numPlayers,
        type=int)
    parser.add_argument(
        "-c", "--client",
        help="Specifies one or more clients to run. " +
        "Example: ./gamerunner.py -p 3 -c myClient -c python " +
        "The gamerunner will run a number of default clients (location optionally"
        "specified with -d) equal to players - specified clients",
        action="append")
    parser.add_argument(
        "-d", "--defaultClient",
        help="The default client to use when others aren't specified."
        "Default: {0}".format(miscConstants.defaultClient),
        default=os.path.join(*miscConstants.defaultClient.split("/")))

    parser.add_argument(
        "-v", "--verbose",
        help="Print player 1's standard output.",
        const=None,
        default=FNULL,
        action="store_const")
    parser.add_argument(
        "-vv", "--veryVerbose",
        help="Prints all players' standard output.",
        const=None,
        default=FNULL,
        action="store_const")

    parser.add_argument(
        "-b", "--scoreboard",
        help="Display the scoreboard in a window.",
        const=True,
        default=False,
        action="store_const")
    parser.add_argument(
        "--scoreboard-url",
        help="Connect to a running scoreboard server.",
        default=None)

    parser.add_argument(
        "-s", "--show",
        help="Display the visualizer in a window.",
        const=True,
        default=False,
        action="store_const")
    parser.add_argument(
        "-th", "--turnsinhour",
        help="Set the game's length.",
        default=0,
        type=int)

    args = parser.parse_args()
    if args.teams < 2:
        sys.stdout.write(parser.format_usage())
        print "{0}: error: Cannot run with less than two players".format(
            parser.prog)
        exit(1)
    if args.client and len(args.client) > args.teams:
        sys.stdout.write(parser.format_usage())
        print "{0}: error: More clients specified than players".format(
            parser.prog)
        exit(1)
    return args


# A simple logger that writes things to a file and, if enabled, to the visualizer
class FileLogger(object):

    def __init__(self, fileName):
        self.file = fileName
        self.vis = False
        self.scoreboard = False

    # The function that logs will be sent to
    # @param stuff
    #   The stuff to be printed
    def print_stuff(self, stuff):
        with open(self.file, 'a') as f:
            f.write(stuff + '\n')
        if self.vis:
            self.vis.add_turn(json.loads(stuff))


''' def test_game(team, team_dir, port):
    client_list = list()
    global parameters
    parameters = parse_args()
    fileLog = FileLogger(team + parameters.log)
    with open(team + parameters.log, 'w'):
        pass
    my_game = game.Game(parameters.map, 2, rooms)
    serv = MMServer(parameters.teams,
                    my_game,
                    logger=fileLog) 
    serv.run(port, partial(launch_client_test_game, team_dir, port), time_out=60)
    return True '''


def main():
    global parameters
    parameters = parse_args()
    sys.stdout.write("Creating server with {0} players, ".format(
        parameters.teams))
    print "and {0} as the map\n".format(parameters.map)
    print "Running server on port {0}\n".format(parameters.port)
    print "Writing log to {0}".format(parameters.log)
    with open(parameters.log, 'w'):
        pass
    fileLog = FileLogger(parameters.log)
    if parameters.show:
        fileLog.vis = VisualizerThread("src/gamerunner/map.json", parameters.debug_view, parameters.scoreboard)
        fileLog.vis.start()
    print "Starting Game"
    my_game = game.Game(parameters.map, parameters.turnsinhour)
    serv = MMServer(parameters.teams,
                    my_game,
                    logger=fileLog)
    serv.run(parameters.port, launch_clients)
    if parameters.show:
        fileLog.vis.join()
    if parameters.scoreboard:
        fileLog.score.stop()


class VisualizerThread(threading.Thread):

    def __init__(self, _mapJsonFileName, _debug=False, _scoreboard=False):
        super(VisualizerThread, self).__init__()
        self.running = False
        self.mapJsonFileName = _mapJsonFileName
        self.debug = _debug
        self.scoreboard = _scoreboard
        self.append_turn = []

    def run(self):
        try:
            with open(self.mapJsonFileName) as json_file:
                mapJsonObject = loadJson(json_file)
            if(mapJsonObject is None):
                raise Exception
        except IOError:
            print("File " + self.mapJsonFileName + " does not exist")
            raise
            exit(1)
        except Exception:
            print("Failed to parse map json data")
            raise
            exit(1)

        self.visualizer = Visualizer(mapJsonObject, self.debug)
        if self.scoreboard:
            self.scoreboard = ScoreboardThread(self.debug)
            self.scoreboard.run()

        while 1:
            if len(self.append_turn) != 0:
                self.visualizer.add_turn(self.append_turn.pop())
            turn = self.visualizer.run()
            if turn is not None:
                if self.scoreboard:
                    self.scoreboard.change_turn(turn)

    def add_turn(self, json):
        self.append_turn.append(json)
        if self.scoreboard:
            self.scoreboard.add_turn(json)

    def kill(self):
        pass

    def stop(self):
        pass

    def __del__(self):
        self.kill()


class ScoreboardThread(threading.Thread):

    def __init__(self, _debug=False):
        super(ScoreboardThread, self).__init__()
        self.running = False
        self.debug = _debug
        self.append_turn = []
        self.turn = 0

    def run(self):
        self.scoreboard = Scoreboard(self.debug)
        last_turn = 0
        while 1:
            if len(self.append_turn) != 0:
                self.scoreboard.add_turn(self.append_turn.pop())
            if last_turn != self.turn:
                self.scoreboard.change_turn(self.turn)
                last_turn = self.turn
            self.scoreboard.run()

    def add_turn(self, json):
        self.append_turn.append(json)

    def change_turn(self, turn_number):
        self.turn = turn_number

    def kill(self):
        pass

    def stop(self):
        pass

    def __del__(self):
        self.kill()


class Client_program(object):

    """
    This object holds and manages the processes for the
    connecting teams
    """
    first = True

    def __init__(self, client_path, port=None):
        """
        path of the client to run
        """
        self.client_path = client_path
        self.port = port

    def run(self):
        """
        """
        try:
            self.bot = Popen(["sh", os.path.join(self.client_path, "run.sh"),
                              "localhost", str(self.port or parameters.port)],
                             stdout=self.chose_output(), cwd=self.client_path)
        except OSError as e:
            msg = "the player {} failed to start with error {}".format(
                self.client_path, e)
            print msg
            raise ClientFailedToRun(msg)

    def kill(self):
        if not self.bot.poll():
            try:
                self.bot.kill()
            except OSError:
                pass

    def stop(self):
        try:
            self.bot.terminate()
        except OSError:
            pass

    @classmethod
    def chose_output(cls):
        output = parameters.veryVerbose
        if cls.first and parameters.veryVerbose == FNULL:
            output = parameters.verbose

        cls.first = False
        return output


class ClientFailedToRun(Exception):

    def __init__(self, msg):
        self.msg = msg

    def __str__(self):
        return self.msg


if __name__ == "__main__":
    main()
