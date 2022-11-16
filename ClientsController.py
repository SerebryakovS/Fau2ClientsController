#!/usr/bin/python
https://github.com/SerebryakovS/Fau2ClientsController.git
import os
import time
import random
import speedtest
import netifaces
from socket import *
import multiprocessing as mp

wlx3460f902a196

COUNT_DEVICES = 10
IfaceNames = [f"wlan{Idx}" for Idx in range(1,COUNT_DEVICES+1)]

#########################################################################################
def ConnectToAccessPoint(ESSID: str,Password: str, IfaceName: str)-> bool:
    os.system(f"nmcli device wifi connect {ESSID} password {Password} ifname {IfaceName}")
def DisconnectFromAccessPoint(IfaceName: str)-> bool:
    os.system(f"nmcli dev disconnect {IfaceName}")
def GetInterfaceIpAddress(IfaceName: str)-> str:
    return netifaces.ifaddresses(IfaceName)[netifaces.AF_INET][0]['addr']
#########################################################################################
def SpeedPrettyFormat(NumberOfBytes:float)-> dict:
    Suffixes = ['B','K','M','G']
    Idx = 0
    while NumberOfBytes >= 1024 and Idx < len(Suffixes)-1:
        NumberOfBytes /= 1024.
        Idx += 1
    return {"value":round(NumberOfBytes,2), "suffix":Suffixes[Idx]}

def SpeedTestGlobal(IfaceName: str)-> dict:
    SoureceIpAddress = GetInterfaceIpAddress(IfaceName)
    SpeedTester = speedtest.Speedtest(source_address=SoureceIpAddress)
    return {
        "Download" : SpeedPrettyFormat(SpeedTester.download()),
        "Upload" : SpeedPrettyFormat(SpeedTester.upload())
    }
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

if __name__ == "__main__":
    # print(SpeedTestGlobal("wlan0"))

    ConnectToAccessPoint("CumanAP","12345678","wlan1")
    # time.sleep(3)
    ConnectToAccessPoint("CumanAP","12345678","wlan2")
    # time.sleep(3)

    # MultiIfaceSpeedTest("wlan1","wlan2")

    # DisconnectFromAccessPoint("wlan1")
    # DisconnectFromAccessPoint("wlan2")







