#!/usr/bin/python2
import socket
import json
import random
import sys

# Python terminal colors; useful for debugging
# Make sure to concat a "printColors.RESET" to the end of your statement!
class printColors:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    RESET = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

# Debugging function
def log(x,c=printColors.BLUE):
    pass
    sys.stderr.write(c + str(x) + printColors.RESET + "\n")

# Set initial connection data
def initialResponse():
    # @competitors YOUR CODE HERE
    return {'teamName':'ubot1'}

# Determine actions to take on a given turn, given the server response
def processTurn(serverResponse):
    # @competitors YOUR CODE HERE

    # Helpful variables
    actions = []
    myId = serverResponse["playerInfo"]["id"]
    myNodes = [x for x in serverResponse["map"] if x["owner"] == myId]
    myP = sum(x["processingPower"] for x in myNodes)
    myN = sum(x["networkingPower"] for x in myNodes)

    # AI variables
    bestScore = 0
    target = None
    action = "control"
    PHASE = []

    # Node lists
    attackedNodes = [x for x in myNodes if max(x["infiltration"]) != 0]

    otherNodes = [x for x in serverResponse["map"]
                  if x["owner"] != myId and x["isIPSed"] == False and not x["isDDoSed"]]

    dangerNodes = [x for x in serverResponse["map"]
                   if x["owner"] != myId
                   if max({k: v for k, v in x["infiltration"].items()
                           if k != str(myId)}) != 0]

    # Creation of dict to maintain the amount of things we own

    # Construct specific otherNodes
    other_small = []
    other_medium = []
    other_large = []
    other_data = []
    other_isp = []
    other_not_rootkit = []

    log("constructing nodes...")
    for node in otherNodes:
        if node["nodetype"] == "Small City":
            other_small.append(node)
        elif node["nodetype"] == "Medium City":
            other_medium.append(node)
        elif node["nodetype"] == "Large City":
            other_large.append(node)
        elif node["nodetype"] == "Data Center":
            other_data.append(node)
        elif node["nodetype"] == "ISP":
            other_isp.append(node)
        else:
            log(node["nodetype"])

        if len(node["rootkits"]) > 0:
            log(node["rootkits"])
        else:
            other_not_rootkit.append(node)

    # Determine PHASE
    if len(attackedNodes) is not 0:
        PHASE.append("DEFEND")
    
    log(len(otherNodes))
    for n in otherNodes:

        if n["nodetype"] == "Small City":
            log("found small node")

            req = n["totalPower"] / 5

            if myN < req or myP < req:
                continue
            else:
                log("rootkiting node")
                actions.append({
                    "action": "rootkit",
                    "target": n["id"]
                })

    
    #log("Player {} P {} / N {}".format(myId, myP, myN))
    #log("MINE " + str([x["id"] for x in myNodes]))
    #log("VIS  " + str([x["id"] for x in otherNodes]))

    ###################################################################################
    # IDEA:                                                                           #
    # Split this bot up into 3 "PHASES" where each "PHASE" has a different trigger    #
    # Condition.                                                                      #
    #                                                                                 #
    # Phase 1 - Greedy, optimized                                                     #
    #    In this phase we attempt to spread very quickly. We attempt to do this until #
    #    Contact is established between a player                                      #
    #                                                                                 #
    #    1. Attempt to maximize taking nodes (tries to take the largest node it can)  #
    #    2. Uses the remaining to try rootkiting more important adjacent nodes        #
    #                                                                                 #
    # Phase 2 - DDoS, Rootkit, upgrade chain                                          #
    ###################################################################################

    
    
    
    

    # Send actions to the server
    return {
        'teamName': 'ubot1',
        'actions': actions
    }

# Main method
# @competitors DO NOT MODIFY
if __name__ == "__main__":

    # Config
    conn = ('localhost', 1337)
    if len(sys.argv) > 2:
        conn = (sys.argv[1], int(sys.argv[2]))

    # Handshake
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(conn)

    # Initial connection
    s.sendall(json.dumps(initialResponse()) + '\n')

    # Initialize test client
    game_running = True
    members = None

    # Run game
    data = s.recv(1024)
    while len(data) > 0 and game_running:
        value = None
        if "\n" in data:
            data = data.split('\n')
            if len(data) > 1 and data[1] != "":
                data = data[1]
                data += s.recv(1024)
            else:
                value = json.loads(data[0])

                # Check game status
                if 'winner' in value:
                    game_running = False

                # Send next turn (if appropriate)
                else:
                    msg = processTurn(value) if "map" in value else initialResponse()
                    s.sendall(json.dumps(msg) + '\n')
                    data = s.recv(1024)
        else:
            data += s.recv(1024)
    s.close()
