
import os
import json
import time
import wget

def ProvideConstantLoad(IfaceName: str):
    with open("Config.json", "r") as JsonConfigFile:
        AppConfig = json.load(JsonConfigFile)["ConstantLoader"]
    LoopLoadFileURL = AppConfig["LoopLoadFileURL"]
    os.system(f"wondershaper {IfaceName} {AppConfig["TargetSpeedDownload"]} {AppConfig["TargetSpeedUpload"]}")
    SuccessfulIterationsCount = 0
    while(1):
        StartTime = time.time()
        Filename = wget.download(LoopLoadFileURL)
        os.system(f"rm {Filename}")
        SuccessfulIterationsCount+=1
        ElapsedTime = time.time() - StartTime
        print(f" IterationsCount={SuccessfulIterationsCount}, ElapsedTime={int(ElapsedTime)}")
