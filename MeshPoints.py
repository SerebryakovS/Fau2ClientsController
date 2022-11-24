#!/usr/bin/python3

import json
import binascii

def AddToMacAddress(MacAddress: str, NumberToAdd: int)-> str:
    BssidUnpretty = str(hex(int(MacAddress.replace(":",""),16) + NumberToAdd))[2:].upper()
    return ':'.join(BssidUnpretty[Idx:Idx+2] for Idx in range(0, len(BssidUnpretty), 2))


class MeshInformator(object):
    def __init__(self):
        with open("Config.json", "r") as JsonConfigFile:
            AppConfig = json.load(JsonConfigFile)["MeshPoints"]
        BaseBssid = AppConfig["BaseBssid"]
        self.MeshPoints = dict()
        for Idx in range(1,AppConfig["TotalCount"]+1):
            self.MeshPoints.update({"MeshDev"+str(Idx) : MeshPoint(AddToMacAddress(BaseBssid, (Idx-1)*2))})


class MeshPoint(object):
    def __init__(self, PointBaseBssid):
        self.PointBaseBssid = PointBaseBssid
        self.Wlan0Bssid = AddToMacAddress(self.PointBaseBssid, 3)
        self.Mesh0Bssid = AddToMacAddress(self.PointBaseBssid, 4)
        self.Wlan1Bssid = self.Mesh0Bssid.replace(self.PointBaseBssid[:2],PointBaseBssid[:1]+"A")
        self.Report = {
            "PointBaseBssid:" : self.PointBaseBssid,
            "Wlan0Bssid" : self.Wlan0Bssid,
            "Wlan1Bssid" : self.Wlan1Bssid,
            "Mesh0Bssid" : self.Mesh0Bssid
        }

if __name__ == "__main__":
    MeshInformator = MeshInformator()
    for MeshPointName in MeshInformator.MeshPoints.keys():
        print(MeshInformator.MeshPoints[MeshPointName].Report)


