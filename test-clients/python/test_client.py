#!/usr/bin/python2
import socket
import json
import random
import sys

if __name__ == "__main__":
    if len(sys.argv) > 2:
        HOST = sys.argv[1]
        PORT = int(sys.argv[2])
    else:
        HOST = 'localhost'
        PORT = 8080
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((HOST, PORT))
    s.sendall('initial_connection\n')
    data = s.recv(1024)
    game_running = True
    members = None
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
                if 'winner' in value:
                    game_running = False
                else:
                    s.sendall('new_turn'+'\n')
                    data = s.recv(1024)
        else:
            data += s.recv(1024)
    s.close()
