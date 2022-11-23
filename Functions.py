#!/usr/bin/python

import time
import random
from socket import *
import multiprocessing as mp

#########################################################################################
def BandwidthServer(IfaceServerName: str, ServerIpAddress: str, Port: int, BufferSize: int):
    StreamSocket = socket(AF_INET, SOCK_STREAM)
    StreamSocket.setsockopt(socket.SOL_SOCKET, SO_BINDTODEVICE, IfaceServerName)
    StreamSocket.bind((ServerIpAddress, Port))
    StreamSocket.listen(1)
    TotallyReceived = 0
    while 1:
        Connection, (Host, RemotePort) = StreamSocket.accept()
        while 1:
            ReceivedData = Connection.recv(BufferSize)
            if not ReceivedData:
                break
            TotallyReceived += len(ReceivedData)
        Connection.close()
        print ('Done with', Host, 'port', RemotePort)

def BandwidthClient(IfaceClientName: str, ServerIpAddress: str, Port: int, BufferSize: int, IterationsCount: int):
    RandomBytesToSend = random.randombytes(BufferSize)
    StartTime = time.time()
    StreamSocket = socket(AF_INET, SOCK_STREAM)
    StreamSocket.setsockopt(socket.SOL_SOCKET, SO_BINDTODEVICE, IfaceClientName)
    StreamSocket.connect((ServerIpAddress, Port))
    StartTime = time.time()
    while IterationsCount > 0:
        StreamSocket.send(RandomBytesToSend)
        IterationsCount -= 1
    StreamSocket.shutdown(1)
    TimeElapsed = time.time()-StartTime
    print ('Time:', TimeElapsed)
    print ('Bandwidth:', round((BufferSize*IterationsCount*0.001) / TimeElapsed, 3))
    print ('Kb/sec')


def MultiIfaceSpeedTest(IfaceServerName: str,IfaceClientName: str):
    PortNumber = 14322; BufferSize = 1024000; IterationsCount = 1000;
    ServerIpAddress = GetInterfaceIpAddress(IfaceServerName)
    ServerProcess = mp.Process(target=BandwidthServer,args=(IfaceServerName,PortNumber,BufferSize))
    ServerProcess.start()
    BandwidthClient(IfaceClientName, ServerIpAddress, PortNumber, BufferSize, IterationsCount)
    ServerProcess.join()
