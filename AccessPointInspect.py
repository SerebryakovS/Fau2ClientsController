#!/usr/bin/python3

import os
import json
import time
import netifaces
import subprocess
import speedtest

#########################################################################################

def ConnectToAccessPoint(ESSID: str,Password: str, IfaceName: str)-> bool:
    os.system(f"nmcli device wifi connect {ESSID} password {Password} ifname {IfaceName}")
    time.sleep(5)
    return

def DisconnectFromAccessPoint(IfaceName: str)-> bool:
    return os.system(f"nmcli dev disconnect {IfaceName}")

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
def InspectAccessPoints(IfaceName: str):
    with open("Config.json", "r") as JsonConfigFile:
        AppConfig = json.load(JsonConfigFile)["AccessPoints"]
    BaseEssid = AppConfig["BaseEssid"]
    for Index in range(1,AppConfig["TotalCount"]+1):
        DisconnectFromAccessPoint(IfaceName)
        ConnectToAccessPoint(BaseEssid+str(Index), AppConfig["Password"], IfaceName)
        print(SpeedTestGlobal(IfaceName),
              "signalPower:",subprocess.getoutput("nmcli -f ACTIVE,SIGNAL dev wifi list | awk '$1==\"yes\" {print $2}'"),"[dBm]")

def BindToAccessPoint(IfaceName: str, AccessPointIndex: str):
    with open("Config.json", "r") as JsonConfigFile:
        AppConfig = json.load(JsonConfigFile)["AccessPoints"]
    EssidToConnect = AppConfig["BaseEssid"] + AccessPointIndex
    DisconnectFromAccessPoint(IfaceName)
    ConnectToAccessPoint(EssidToConnect, AppConfig["Password"], IfaceName)




