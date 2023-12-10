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

from EASLogger import EASloggerSingleton


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

class receiveReward:
    def __init__(self, adb_path, adb_port):
        self.adb_path = adb_path
        self.adb_port = adb_port



    def run(self):
        adb_is_connected = ADBClass.AdbSingleton.getInstance().connectDevice(adb_path=self.adb_path,
                                                                             adb_port=self.adb_port,
                                                                             retryCount=20)
        SetupAdbFlow = SetupAdb(adb_path=self.adb_path, adb_port=self.adb_port, retry_count=5)
        SetupAdbFlow.run()
        EASloggerSingleton.getInstance().info('./logs/log_test.txt', "開始收獎勵")
        OctoUtil.OctoUtil.backToMainScreen()


        ADBClass.AdbSingleton.getInstance().screen_capture('./img/rewardIconCheck.png')
        cvres = OctoUtil.OctoUtil.cv2CheckImgExist('./Icons/RewardIcon.png', './img/rewardIconCheck.png')

        if cvres is not None:
            ADBClass.AdbSingleton.getInstance().tap(cvres)
            time.sleep(2)
            ADBClass.AdbSingleton.getInstance().screen_capture('./img/rewardIconCheck.png')
            cvres = OctoUtil.OctoUtil.cv2CheckImgExist('./Icons/RewardTake.png', './img/rewardIconCheck.png')
            ADBClass.AdbSingleton.getInstance().tap(cvres)

            time.sleep(2)
            ADBClass.AdbSingleton.getInstance().tap((645,555))

            ADBClass.AdbSingleton.getInstance().screen_capture('./img/rewardIconCheck.png')
            cvres = OctoUtil.OctoUtil.cv2CheckImgExist('./Icons/backButton.png', './img/rewardIconCheck.png')
            ADBClass.AdbSingleton.getInstance().tap(cvres)
            EASloggerSingleton.getInstance().info('./logs/log_test.txt', "結束收獎勵")
        return input