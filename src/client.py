#!/usr/bin/env python

import signal
import time
import sys
import numpy as np
import random
import math
import socket

######################################################################
# crea un numpy array di numeri random
input_data = np.random.randint(255, size=500, dtype=np.uint8)

# transforma l'array in una sequenza di byte
data_to_send = input_data.tobytes()

# qui viene gestita la trasmissione con socket UDP:
# - suddividere i dati 
# - mandarli ad un server
# - tenere traccia dei dati ricevuti
# - ripetere periodicamente ogni T secondi (ad esempio, T=0.1)

# Initial params for client and server
SRV_IP = "127.0.0.1"
SRV_PORT = 1337

CLIENT_IP = "127.0.0.1"
CLIENT_PORT = 1338


def handler(sig, frame):
    print("\nKeyboard Interrupt, exiting...\n")
    sndSock.close()
    exit(0)


if __name__ == "__main__":
    sndSock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    rcvSock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    rcvSock.bind((CLIENT_IP, CLIENT_PORT))
    rcvSock.settimeout(0.1)

    signal.signal(signal.SIGINT, handler)

    while True:
        # crea un numpy array di numeri random
        input_data = np.random.randint(255, size=500, dtype=np.uint8)

        # trasforma l'array in una sequenza di byte
        data_to_send = input_data.tobytes()

        print("type: ", input_data)
        sndSock.sendto(data_to_send, (SRV_IP, SRV_PORT))
        time.sleep(0.1)

        print("ACK?")
        try:
            data, addr = rcvSock.recvfrom(1024)
            print(data.decode('utf-8'))
            rcvSock.close()
            exit(0)
        except socket.timeout:
            print("No ACK")
            rcvSock.close()
            exit(0)
