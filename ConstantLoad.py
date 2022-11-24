
import os
import json
import time
import wget

def ProvideConstantLoad(IfaceName: str, DownloadSpeed: str):
    os.system(f"wondershaper clear {IfaceName}")
    time.sleep(1)
    with open("Config.json", "r") as JsonConfigFile:
        AppConfig = json.load(JsonConfigFile)["ConstantLoader"]
    LoopLoadFileURL = AppConfig["LoopLoadFileURL"]
    os.system(f"wondershaper {IfaceName} -d {int(DownloadSpeed)*1000}")
    time.sleep(1)
    SuccessfulIterationsCount = 0
    while(True):
        StartTime = time.time()
        Filename = wget.download(LoopLoadFileURL)
        os.system(f"rm {Filename}")
        SuccessfulIterationsCount+=1
        ElapsedTime = time.time() - StartTime
        print(f" IterationsCount={SuccessfulIterationsCount}, ElapsedTime={int(ElapsedTime)}")
ProvideConstantLoad("wlan0","20")
