#!/usr/bin/env python

import signal
import time
import sys
import numpy as np
import random
import math
import socket

######################################################################
# Lato server, bisogna gestire la ricezione dei dati:
# - collezionar ei vari pezzi
# - riassemblarli
# - mandare un ACK di livello applicativo se ricevuti tutti

# per ricostruire l'array numpy dai dati ricevuti si usa "frombuffer"
# applicato a "received_data"
# rebuilt_data = np.frombuffer(received_data, dtype=np.uint8)

# Server - client sock config: 

SRV_IP = "127.0.0.1"
SRV_PORT = 1337

CLIENT_IP = "127.0.0.1"
CLIENT_PORT = 1338


# Keyboard Interrupt handler to close as gracefully as possible:
def handler(sig, frame):
    print("\nKeyboard Interrupt, exiting...\n")
    sndSock.close()
    exit(0)


if __name__ == "__main__":
    # server-side socket opening and set up:
    sndSock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sndSock.bind((SRV_IP, SRV_PORT))
    sndSock.settimeout(0.05)
    signal.signal(signal.SIGINT, handler)

    # client-side socket config for ACK
    rcvSock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    while True:
        try:
            data, addr = sndSock.recvfrom(1024)
            received = np.array(np.frombuffer(data, dtype=np.uint8))
            print("Message: ", received)
            rcvSock.sendto("ACK!".encode('utf-8'), (CLIENT_IP, CLIENT_PORT))
            print("ACK sent")
        except socket.timeout:
            pass
