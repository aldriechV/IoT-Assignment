import socket
import ipaddress
import threading
import time
import contextlib
import errno
from dataclasses import dataclass
import random
import sys
from collections.abc import MutableMapping

maxPacketSize = 1024
defaultPort = 12345 #TODO: Set this to your preferred port
exitSignal = False

def GetFreePort(minPort: int = 1024, maxPort: int = 65535):
    for i in range(minPort, maxPort):
        print("Testing port",i);
        with contextlib.closing(socket.socket(socket.AF_INET, socket.SOCK_STREAM)) as potentialPort:
            try:
                potentialPort.bind(('localhost', i));
                potentialPort.close();
                print("Server listening on port",i);
                return i
            except socket.error as e:
                if e.errno == errno.EADDRINUSE:
                    print("Port",i,"already in use. Checking next...");
                else:
                    print("An exotic error occurred:",e);

def GetServerData() -> []:
    import MongoDBConnection as mongo
    return mongo.QueryDatabase();

def ListenOnTCP(tcpSocket: socket.socket, socketAddress):
    while True:
      # Accept incoming connection
      try:
      # Receive data from client
        while True:
          data = tcpSocket.recv(1024)
          if not data:
            break
          print("Received data from client:", data.decode())
          data = GetServerData();
          avg = 0
          current_road = ""
          for road, road_data in data.items():
            if avg == 0:
                avg = road_data['freewayTime'] / road_data['count']
                current_road = road
            elif avg < road_data['freewayTime'] / road_data['count']:
                avg = road_data['freewayTime'] / road_data['count']
                current_road = road
          servermessage = "The best road to take is " + current_road + " with an average time of " + str(avg)
          tcpSocket.sendall(servermessage.encode())
      finally:
              print("Connection closed")
              #Close server socket
              tcpSocket.close()
      break
def CreateTCPSocket() -> socket.socket:
    tcpSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM);
    tcpPort = defaultPort
    print("TCP Port:",tcpPort);
    tcpSocket.bind(('localhost', tcpPort));
    return tcpSocket;

def LaunchTCPThreads():
    tcpSocket = CreateTCPSocket();
    tcpSocket.listen(5);
    while True:
        connectionSocket, connectionAddress = tcpSocket.accept();
        connectionThread = threading.Thread(target=ListenOnTCP, args=[connectionSocket, connectionAddress]);
        connectionThread.start();

if __name__ == "__main__":
    tcpThread = threading.Thread(target=LaunchTCPThreads);
    tcpThread.start();

    while not exitSignal:
        time.sleep(1);
    print("Ending program by exit signal...");
