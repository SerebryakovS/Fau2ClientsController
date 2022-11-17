#!/usr/bin/python

import json
import binascii

def AddToMacAddress(MacAddress: str, NumberToAdd: int)-> str:
    BssidUnpretty = str(hex(int(MacAddress.replace(":",""),16) + NumberToAdd))[2:].upper()
    return ':'.join(BssidUnpretty[Idx:Idx+2] for Idx in range(0, len(BssidUnpretty), 2))


class MeshInformator(object):
    def __init__(self):
        with open("Config.json", "r") as JsonConfigFile:
            AppConfig = json.load(JsonConfigFile)["MeshPoints"]
        StartBaseBssid = AppConfig["StartBaseBssid"]
        self.MeshPoints = dict()
        for Idx in range(1,AppConfig["TotalCount"]+1):
            self.MeshPoints.update({"MeshDev"+str(Idx) : MeshPoint(AddToMacAddress(StartBaseBssid, (Idx-1)*2))})

class MeshPoint(object):
    def __init__(self, PointBaseBssid):
        self.PointBaseBssid = PointBaseBssid
        self.Wlan0Bssid = AddToMacAddress(self.PointBaseBssid, 3)
        self.Wlan1Bssid = AddToMacAddress(self.PointBaseBssid, 4)
        print(self.PointBaseBssid,self.Wlan0Bssid,self.Wlan1Bssid)

if __name__ == "__main__":
    m = MeshInformator()


