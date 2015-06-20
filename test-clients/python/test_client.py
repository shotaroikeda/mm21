#!/usr/bin/python2
import socket
import json
import random
import sys

# Set initial connection data
def initialResponse():
    # @competitors YOUR CODE HERE
    return {'team':'test'}

# Actions to take on a given turn
def processTurn():
    # @competitors YOUR CODE HERE
    return {
        'team': 'test',
        'actions': [],
        'these-are': 'sample-values'
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
                #print 'Received', repr(data[0])

                # Check game status
                if 'winner' in value:
                    game_running = False

                # Send next turn (if appropriate)
                else:
                    s.sendall(json.dumps(processTurn(value)) + '\n')
                    data = s.recv(1024)
        else:
            data += s.recv(1024)
    s.close()
