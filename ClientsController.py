#!/usr/bin/python3

# https://github.com/SerebryakovS/Fau2ClientsController.git

import os
import argparse
import AccessPointInspect
import ConstantLoad

if __name__ == "__main__":
    ArgumentsParser = argparse.ArgumentParser(formatter_class = argparse.RawDescriptionHelpFormatter)
    ArgumentsParser.add_argument("-i", "--inspect", metavar="INSPECT", help = "Inspect all provided access points for speed and power")
    ArgumentsParser.add_argument("-d", "--download", metavar="DWNLOAD", help = "Infinite downloading with rate specified in config file")
    Arguments = vars(ArgumentsParser.parse_args())
    if Arguments["inspect"]:
        AccessPointInspect.InspectAccessPoints(Arguments["inspect"])
    if Arguments["download"]:
        ConstantLoad.ProvideConstantLoad(Arguments["download"])


