import time

import cv2
import numpy as np

import ADBClass
from OctoUtil import OctoUtil


class StartApp:
    def __init__(self, adb_path, adb_port):
        self.adb_path = adb_path
        self.adb_port = adb_port

    def run(self):
        res = ADBClass.AdbSingleton.getInstance().getAllPackages()
        print(" avalible package", res)

        if ADBClass.AdbSingleton.APP_PACKAGE in res:
            ADBClass.AdbSingleton.getInstance().startApp()
            return True
        else:
            print("App not found")
            return False

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

class screenshot_cv2_match_template_login:
    def __init__(self, screenshot, icon, retry_count, subpattern, current_stage):
        self.screenshot = screenshot
        self.icon = icon
        self.retry_count = retry_count
        self.subpattern = subpattern
        self.current_stage = current_stage
    def run(self):
        isValid = False
        tap_pos = (0, 0)
        cv2_img_screenshot_rect = (0, 0, 0, 0)
        cv2_img_screenshot_result = (0, 0, 0, 0)
        while isValid is False:
            ADBClass.AdbSingleton.getInstance().screen_capture(self.screenshot)
            screenshot = cv2.imread(self.screenshot, 0)
            pattern = cv2.imread(self.icon, 0)
            result = cv2.matchTemplate(pattern, screenshot, cv2.TM_CCOEFF_NORMED)
            threshold = 0.8

            # Find the location of matched regions above the threshold
            locations = np.where(result >= threshold)

            # Draw rectangles around the matched regions
            for pt in zip(*locations[::-1]):
                cv2.rectangle(screenshot, pt, (pt[0] + pattern.shape[1], pt[1] + pattern.shape[0]), (255, 255, 0), 2)

            # Display the result
            # cv2.imshow('Result', screenshot)
            # cv2.waitKey(0)
            # cv2.destroyAllWindows()
            if len(locations[0]) > 0:
                isValid = True
                print("There is a result.")
                x, y = locations[::-1]
                w, h = pattern.shape[::-1]
                cv2_img_screenshot_rect = (x[0], y[0], w, h)
                tap_pos = (x[0] + w / 2, y[0] + h / 2)
            else:
                print("There is no result.")
                # try subPattern cv, if res is not empty, set output to subpattern related result, then skip to the desired
                # node, where subpatterns should be key value pair, key is the subpattern, value is the result action, then
                # breaks the retry by returning True in the verification function
                # SAMPLE:
                subPattern = self.subpattern
                if subPattern is not None:
                    for subPattern in subPattern:
                        print("subPattern: ", subPattern)
                        cv_screenshot = cv2.imread(subPattern["subPattern"], 0)
                        subPatternResult = cv2.matchTemplate(cv_screenshot, screenshot, cv2.TM_CCOEFF_NORMED)
                        subPatternThreshold = 0.8
                        subPatternLocations = np.where(subPatternResult >= subPatternThreshold)
                        if len(subPatternLocations[0]) > 0:
                            isValid = True
                            print("There is a sub pattern result.")
                            self.current_stage = subPattern["targetStage"]
                            subPatternRes = True
                            break
                        else:
                            subPatternRes = False
                            print("There is no sub pattern.")
                else:
                    subPatternRes = False
                    print("There is no sub pattern.")
            cv2_img_screenshot_result = locations
        return (tap_pos, cv2_img_screenshot_rect, cv2_img_screenshot_result)

class loginReward:
    def __init__(self):
        pass
    def run(self):
        isLoading = True
        while isLoading is True:
            ADBClass.AdbSingleton.getInstance().screen_capture('./img/loginReward.png')
            screenshot = cv2.imread('./img/loginReward.png', 0)
            isSpeedAnimation = OctoUtil.check_pixel_color('./img/loginReward.png', 751, 35,
                                                                   (45, 49, 60, 255))
            if isSpeedAnimation is False:
                isLoading = False
            time.sleep(2)
        time.sleep(10)

        ADBClass.AdbSingleton.getInstance().screen_capture('./img/loginRewardDailyCheck.png')
        res = self.cv2CheckImgExist('./Icons/RewardPopUp.png', './img/loginRewardDailyCheck.png')
        print("cv2 result (MATERIAL_MENU): ", res)
        if res:
            ADBClass.AdbSingleton.getInstance().tap((640, 630))
            time.sleep(1)
            ADBClass.AdbSingleton.getInstance().screen_capture('./img/loginRewardDailyCheck.png')
            res = self.cv2CheckImgExist('./Icons/dailyBulletinClose.png', './img/loginRewardDailyCheck.png')
            if res:
                ADBClass.AdbSingleton.getInstance().tap(res)
                time.sleep(1)
        return True

    def cv2CheckImgExist(self, patternPath, screenshotPath):
        screenshot = cv2.imread(screenshotPath, 0)
        pattern = cv2.imread(patternPath, 0)
        result = cv2.matchTemplate(pattern, screenshot, cv2.TM_CCOEFF_NORMED)
        threshold = 0.8

        # Find the location of matched regions above the threshold
        locations = np.where(result >= threshold)

        # Draw rectangles around the matched regions
        # for pt in zip(*locations[::-1]):
        #     cv2.rectangle(screenshot, pt, (pt[0] + pattern.shape[1], pt[1] + pattern.shape[0]), (255, 255, 0), 2)
        #
        # cv2.imshow('Result', screenshot)
        # cv2.waitKey(0)
        # cv2.destroyAllWindows()
        # Display the result
        # cv2.imshow('Result', screenshot)
        # cv2.waitKey(0)
        # cv2.destroyAllWindows()
        if len(locations[0]) > 0:
            x, y = locations[::-1]
            w, h = pattern.shape[::-1]
            return (x[0] + w / 2, y[0] + h / 2)
        else:
            return None


class runStartApp:
    def __init__(self, adb_path, adb_port):
        self.adb_path = adb_path
        self.adb_port = adb_port
        self.currentStage = 0
    def run(self):
        adb_is_connected = ADBClass.AdbSingleton.getInstance().connectDevice(adb_path=self.adb_path, adb_port=self.adb_port,
                                                                retryCount=20)
        SetupAdbFlow = SetupAdb(adb_path=self.adb_path, adb_port=self.adb_port, retry_count=5)
        SetupAdbFlow.run()
        StartAppFlow = StartApp(adb_path=self.adb_path, adb_port=self.adb_port)
        StartAppFlow.run()

        time.sleep(5)
        #"parameters" is currentlt useless
        loginBulletinCloseFlow = screenshot_cv2_match_template_login(screenshot="./img/loginCapture.png", icon="./Icons/loginBulletinClose.png", retry_count=5, subpattern=
            [
                  {
                      "subPattern": "./Icons/loginStartGame.png",
                      "targetStage": 1,
                      "parameters": "cv_login_click_node_login"
                  },
                  {
                      "subPattern": "./Icons/loggedInCheckImg.png",
                      "targetStage": 2,
                      "parameters": "FinalSleepNode"
                  }
            ]
            , current_stage=self.currentStage
        )
        res = loginBulletinCloseFlow.run()
        if self.currentStage != loginBulletinCloseFlow.current_stage:
            self.currentStage = loginBulletinCloseFlow.current_stage
        else:
            ADBClass.AdbSingleton.getInstance().tap(res[0])
        if self.currentStage < 1:
            loginButtonFlow = screenshot_cv2_match_template_login(screenshot="./img/loginButtonCapture.png",
                                                        icon="./Icons/loginStartGame.png", retry_count=5, subpattern=
                 [
                     {
                         "subPattern": "./Icons/loggedInCheckImg.png",
                         "function": 2,
                         "parameters": "FinalSleepNode"
                     }
                 ]
                 , current_stage=self.currentStage
            )
            res = loginButtonFlow.run()
            if self.currentStage != loginBulletinCloseFlow.current_stage:
                self.currentStage = loginBulletinCloseFlow.current_stage
            else:
                ADBClass.AdbSingleton.getInstance().tap(res[0])
        if self.currentStage < 2:
            time.sleep(10)
            loginRewardFlow = loginReward()
            loginRewardFlow.run()