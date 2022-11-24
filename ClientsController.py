#!/usr/bin/python3

# https://github.com/SerebryakovS/Fau2ClientsController.git

import os
import json
import argparse
import AccessPointInspect
import ConstantLoad

if __name__ == "__main__":
    ArgumentsParser = argparse.ArgumentParser(formatter_class = argparse.RawDescriptionHelpFormatter)
    ArgumentsParser.add_argument("-b", "--bind", metavar="BIND", help = "Bind execution to specific access point (by index: [1,2,3])")
    ArgumentsParser.add_argument("-i", "--inspect", metavar="INSPECT", help = "Inspect all provided access points for speed and power")
    ArgumentsParser.add_argument("-d", "--download", metavar="DWNLOAD", help = "Infinite downloading with rate specified in config file")
    Arguments = vars(ArgumentsParser.parse_args())
    with open("Config.json", "r") as JsonConfigFile:
        IfaceName = json.load(JsonConfigFile)["NetworkInterface"]
    if Arguments["bind"]:
        AccessPointInspect.BindToAccessPoint(IfaceName,AccessPointIndex)
    if Arguments["inspect"]:
        AccessPointInspect.InspectAccessPoints(IfaceName)
    if Arguments["download"]:
        ConstantLoad.ProvideConstantLoad(IfaceName)
