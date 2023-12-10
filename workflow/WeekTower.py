import math
import re
import time

import cv2
import yaml
from PIL import Image

import OCRClass
import OctoUtil
import ADBClass
import numpy as np
from PIL import ImageChops


class SetupAdb:
    def __init__(self, adb_path, adb_port, retry_count):
        self.adb_path = adb_path
        self.adb_port = adb_port
        self.retry_count = retry_count

    def run(self):
        def node_setup_adb(self):
            res = ADBClass.AdbSingleton.getInstance().connectDevice(adb_path=self.adb_path,
                                                                    adb_port=self.adb_port,
                                                                    retryCount=self.retry_count)
            return res

class NavigateToTower:
    def __init__(self):
        pass

    def run(self):
        ADBClass.AdbSingleton.getInstance().screen_capture('./img/weeklyTower.png')
        res = OctoUtil.OctoUtil.cv2CheckImgExist('./Icons/loggedInCheckImg.png', './img/weeklyTower.png')
        if res:
            ADBClass.AdbSingleton.getInstance().tap(res)
            time.sleep(1)

        ADBClass.AdbSingleton.getInstance().tap((280,311))
        time.sleep(3)
        ADBClass.AdbSingleton.getInstance().swipe((1176, 377), (101, 377), 1000)
        time.sleep(1)
        ADBClass.AdbSingleton.getInstance().tap((640,334))
        time.sleep(1)

class startFight:
    def __init__(self):
        pass
    def run(self):
        ADBClass.AdbSingleton.getInstance().tap((500, 440))  # tap left
        time.sleep(1)
        ADBClass.AdbSingleton.getInstance().screen_capture('./img/weeklyTower.png')
        res = OctoUtil.OctoUtil.cv2CheckImgExist('./Icons/TowerStartFight.png', './img/weeklyTower.png')
        if res is None:
            ADBClass.AdbSingleton.getInstance().tap((738, 440))  # tap right
            time.sleep(1)
            res = OctoUtil.OctoUtil.cv2CheckImgExist('./Icons/TowerStartFight.png', './img/weeklyTower.png')
            if res is not None:
                ADBClass.AdbSingleton.getInstance().tap(res)
                time.sleep(1)
        else:
            ADBClass.AdbSingleton.getInstance().tap(res)
            time.sleep(1)


class getCurrentProgress:
    def __init__(self):
        pass

    def run(self):
        ADBClass.AdbSingleton.getInstance().screen_capture('./img/weeklyTower.png')
        res = OctoUtil.OctoUtil.cv2CheckImgExist('./Icons/TowerReward.png', './img/weeklyTower.png')
        if res:
            ADBClass.AdbSingleton.getInstance().tap(res)
            time.sleep(1)

        #screencap and crop 741,552 - 806, 592
        ADBClass.AdbSingleton.getInstance().screen_capture('./img/weeklyTower.png')
        im = Image.open('./img/weeklyTower.png')
        im = im.crop((741,552,866,592))
        im.save('./img/weeklyTower.png')
        im.close()

        res = OCRClass.PaddleOCRSingleton.getInstance().scanText('./img/weeklyTower.png')
        print(res)
        # the result is [1-10]/10, and i only want to extract the first number
        res = re.findall(r'\d+', res[0][0])
        res = int(res[0])
        print(res)
        ADBClass.AdbSingleton.getInstance().tap((80,36))
        time.sleep(1)
        return res



class weeklyTower:
    def __init__(self, adb_path, adb_port):
        self.adb_path = adb_path
        self.adb_port = adb_port



    def run(self):
        adb_is_connected = ADBClass.AdbSingleton.getInstance().connectDevice(adb_path=self.adb_path,
                                                                             adb_port=self.adb_port,
                                                                             retryCount=20)
        SetupAdbFlow = SetupAdb(adb_path=self.adb_path, adb_port=self.adb_port, retry_count=5)
        SetupAdbFlow.run()

        OctoUtil.OctoUtil.backToMainScreen()

        NavigateToTowerFlow = NavigateToTower()
        NavigateToTowerFlow.run()
        time.sleep(3)
        getCurrentProgressFlow = getCurrentProgress()
        getCurrentProgressFlow.run()