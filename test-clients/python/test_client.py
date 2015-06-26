#!/usr/bin/python2
import socket
import json
import random
import sys

# Debugging function
def log(x):
    sys.stderr.write(str(x))

# Set initial connection data
def initialResponse():
    # @competitors YOUR CODE HERE
    return {'teamName':'test'}

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

    # Node lists
    attackedNodes = [x for x in myNodes if max(x["infiltration"]) != 0]
    otherNodes = [x for x in serverResponse["map"] if x["owner"] != myId]

    # 1) Defend our nodes under attack
    if len(attackedNodes) != 0:
        for n in attackedNodes:
            score = max(n["infiltration"])*2
            if score > bestScore:
                target = n
                bestScore = score

                # Last stand of the DDoS
                if max(n["infiltration"]) > 0.75*(n["processingPower"] + n["networkingPower"]):
                    action = "ddos"

    # 2) Capture most powerful nearby node (with free ones being slightly worse than taken ones)
    if len(otherNodes) != 0:
        target = otherNodes[0]
        bestScore = 0
        for n in otherNodes:
            score = n["processingPower"] + n["networkingPower"]
            if myP < myN:
                score = n["networkingPower"]
            if myP > myN:
                score = n["processingPower"]

            score = score * 1.25 if n["owner"] != None else score
            if score > bestScore:
                target = n
                bestScore = score
                action = "control"

        actions.append({
            "action": "control",
            "target": target["id"],
            "multiplier": min(myP, myN)
        })

    # Send actions to the server
    return {
        'teamName': 'test',
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
