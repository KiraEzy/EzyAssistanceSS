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




class mainMaterial:
    def __init__(self, adb_path, adb_port):
        self.adb_path = adb_path
        self.adb_port = adb_port
        self.currentStage = 0

    def clickAutoCharacter(self, mission_status, mission_code):
        with open('active_config.yaml', 'r') as file:
            config_data = yaml.safe_load(file)
            # print(config_data[0]['LevelAutomation'][0][mission_code])
            mission_list = config_data[0]['LevelAutomation']
            level_character_list = mission_list[mission_code]['characters']
            level_character = level_character_list.split(',')

        resArr = []
        for char in level_character:
            print(char)
            matches = re.findall(r'"([^"]*)"', char)

            if len(matches) > 0:
                char = matches[0]
                print("Text inside quotation marks:", char)
            ADBClass.AdbSingleton.getInstance().screen_capture('./img/autoRunScreenshot.png')
            res = OCRClass.OCRSingleton.getInstance().findTextPosition('./img/autoRunScreenshot.png', char)
            notRunOunOutOfCharacter = True
            while notRunOunOutOfCharacter:
                if res is not None:
                    left = 970
                    top = 554
                    right = 985
                    bottom = 585
                    inputImgPath = './img/checkSelectedCharNum.png'
                    ADBClass.AdbSingleton.getInstance().screen_capture(inputImgPath)
                    screenshot = Image.open(inputImgPath)
                    cropped_image = screenshot.crop((left, top, right, bottom))
                    cropped_image.save('./img/checkSelectedCharNumBefore.png')

                    OctoUtil.OctoUtil.checkSelectedCharNum(top, left, bottom, right)
                    ADBClass.AdbSingleton.getInstance().tap(res[1])
                    # should add check is really selected to validate the character is avalible
                    time.sleep(1)
                    inputImgPath = './img/checkSelectedCharNum.png'
                    ADBClass.AdbSingleton.getInstance().screen_capture(inputImgPath)
                    screenshot = Image.open(inputImgPath)
                    cropped_image = screenshot.crop((left, top, right, bottom))
                    cropped_image.save('./img/checkSelectedCharNumAfter.png')

                    image_one = Image.open("./img/checkSelectedCharNumBefore.png").convert('RGB')
                    image_two = Image.open("./img/checkSelectedCharNumAfter.png").convert('RGB')

                    diff = ImageChops.difference(image_one, image_two)
                    if diff.getbbox() is not None:
                        time.sleep(1)
                        ADBClass.AdbSingleton.getInstance().swipe((400, 325), (400, 10000), 1000)
                        time.sleep(3)
                        break
                    else:
                        return (f"Character Cannot Be Selected: {char}", res)
                else:
                    # Calculate the crop box coordinates
                    left = 139
                    top = 312
                    right = 607
                    bottom = 428

                    ADBClass.AdbSingleton.getInstance().screen_capture('./img/ScrollCharacterBefore.png')
                    screenshot = Image.open('./img/ScrollCharacterBefore.png')
                    cropped_image = screenshot.crop((left, top, right, bottom))
                    cropped_image.save("./img/ScrollCharacterBeforeCroppedScreenshot.png")

                    ADBClass.AdbSingleton.getInstance().swipe((400, 600), (400, 225), 1000)
                    time.sleep(4)

                    ADBClass.AdbSingleton.getInstance().screen_capture('./img/ScrollCharacterAfter.png')
                    screenshot = Image.open('./img/ScrollCharacterAfter.png')
                    cropped_image = screenshot.crop((left, top, right, bottom))
                    cropped_image.save("./img/ScrollCharacterAfterCroppedScreenshot.png")

                    image_one = Image.open("./img/ScrollCharacterBeforeCroppedScreenshot.png").convert('RGB')
                    image_two = Image.open("./img/ScrollCharacterAfterCroppedScreenshot.png").convert('RGB')

                    diff = ImageChops.difference(image_one, image_two)

                    if diff.getbbox() is not None:
                        print("The images are different.")
                        ADBClass.AdbSingleton.getInstance().screen_capture('./img/autoRunScreenshot.png')
                        time.sleep(2)
                        res = OCRClass.OCRSingleton.getInstance().findTextPosition('./img/autoRunScreenshot.png', char)
                        # if res is None:
                        #     res = OCRClass.OCRSingleton.getInstance().findTextPosition('./img/autoRunScreenshot.png', char)
                        time.sleep(2)

                    else:
                        print("The images are the same.")
                        return ("error", "No character found")

            resArr.append(res)
        if len(resArr) is not len(level_character):
            return ("error", "No character found")
        else:
            return ("success", "Character found")

    def BackBtnClick(self):
        ADBClass.AdbSingleton.getInstance().tap((80, 34))

    def checkCurrentPageStatus(self, destinationPage):
        if "DailyMaterial" in destinationPage[0]:
            ADBClass.AdbSingleton.getInstance().screen_capture('./img/levelCapture.png')
            res = self.cv2CheckImgExist('./Icons/materialMissionCheck.png', './img/levelCapture.png')
            print("cv2 result (MATERIAL_MENU): ", res)
            if res:
                return ("MATERIAL_MENU", res)
            res = self.cv2CheckImgExist('./Icons/loggedInCheckImg.png', './img/levelCapture.png')
            print("cv2 result (HOME): ", res)
            if res:
                return ("HOME", res)
            res = self.cv2CheckImgExist('./Icons/1in3menu.png', './img/levelCapture.png')
            print("cv2 result (ONE_IN_THREE): ", res)
            if res:
                return ("ONE_IN_THREE", res)
            res = self.cv2CheckImgExist('./Icons/backButton.png', './img/levelCapture.png')
            print("cv2 result (OTHER_WITH_BACK_BTN): ", res)
            if res:
                return ("OTHER_WITH_BACK_BTN", res)
            res = self.cv2CheckImgExist('./Icons/backButton.png', './img/levelCapture.png')
            print("cv2 result (OTHER_WITH_BACK_BTN): ", res)
            if res:
                return ("OTHER_WITH_BACK_BTN", res)
            return "OTHER"

    def cv2CheckImgExist(self, patternPath, screenshotPath, isSingle=True):
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
        if isSingle:
            if len(locations[0]) > 0:
                x, y = locations[::-1]
                w, h = pattern.shape[::-1]
                return (x[0] + w / 2, y[0] + h / 2)
            else:
                return None
        else:
            if len(locations[0]) > 0:
                x, y = locations[::-1]
                w, h = pattern.shape[::-1]
                xi = x[0]
                yi = y[0]
                resArr = []
                # loop for locations items times
                for i in range(len(locations[0])):
                    isTooClose = False
                    for coord in resArr:
                        currCoord = (x[i], y[i])
                        dist = math.dist(coord, currCoord)
                        if dist < 50:
                            isTooClose = True
                            break
                    if not isTooClose:
                        resArr.append((x[i] + w / 2, y[i] + h / 2))
                return resArr
            else:
                return None

    def GotoDailyMaterialStep(self, currentStatus, destinationPage):
        currentPage = currentStatus[0]
        print("GotoDailyMaterialStep ||| currentPage: ", currentPage, " | destinationPage: ", destinationPage)
        match currentPage:
            case "ONE_IN_THREE":
                ADBClass.AdbSingleton.getInstance().tap((290, 330))
                return "ONGOING"
            case "HOME":
                ADBClass.AdbSingleton.getInstance().tap(currentStatus[1])
                return "ONGOING"
            case "OTHER_WITH_BACK_BTN":
                ADBClass.AdbSingleton.getInstance().tap(currentStatus[1])
                return "ONGOING"
            case "MATERIAL_MENU":
                if destinationPage[1] is not None:
                    match destinationPage[1]:
                        case "EXP":
                            ADBClass.AdbSingleton.getInstance().tap((645, 470))
                            return "ARRIVED"
                        case "SRD":
                            ADBClass.AdbSingleton.getInstance().tap((410, 366))
                            return "ARRIVED"
                        case "WUP":
                            ADBClass.AdbSingleton.getInstance().tap((1252, 384))
                            return "ARRIVED"
                        case "WEA":
                            ADBClass.AdbSingleton.getInstance().tap((202, 443))
                            return "ARRIVED"
                        case "TRT":
                            ADBClass.AdbSingleton.getInstance().tap((40, 430))
                            return "ARRIVED"
                        case "STAR":
                            ADBClass.AdbSingleton.getInstance().tap((1078, 430))
                            return "ARRIVED"
                        case "ENC":
                            ADBClass.AdbSingleton.getInstance().tap((875, 430))
                            return "ARRIVED"

    def GotoMiddleStep(self, destinationPage):
        print("GotoDifficultyStep ||| destinationPage: ", destinationPage)
        if destinationPage[3] is "multi":
            middleNo = destinationPage[4]
            ADBClass.AdbSingleton.getInstance().screen_capture('./img/GotoMiddleStepScreenshot.png')
            # crop image
            left = 45
            top = 453
            right = 1235
            bottom = 582
            screenshot = Image.open('./img/GotoMiddleStepScreenshot.png')
            cropped_image = screenshot.crop((left, top, right, bottom))
            cropped_image.save("./img/GotoMiddleStepScreenshotCroppedScreenshot.png")

            res = OCRClass.OCRSingleton.getInstance().findTextPosition(
                './img/GotoMiddleStepScreenshotCroppedScreenshot.png', str(middleNo))
            print("res: ", res)
            if res is not None:
                ADBClass.AdbSingleton.getInstance().tap((res[1][0] + left, res[1][1] + top))
                return True
            else:
                cvres = self.cv2CheckImgExist('./Icons/MiddleLevelENCIdentifier.png',
                                              './img/GotoMiddleStepScreenshotCroppedScreenshot.png', False)
                tapPos = (cvres[middleNo - 1][0] + left, cvres[middleNo - 1][1] + top)
                ADBClass.AdbSingleton.getInstance().tap(tapPos)
        return True

    def GotoDifficultyStep(self, destinationPage):
        print("GotoDifficultyStep ||| destinationPage: ", destinationPage)
        time.sleep(2)
        ADBClass.AdbSingleton.getInstance().screen_capture('./img/gotoDifficultyStepCapture.png')
        screenshot = Image.open("./img/gotoDifficultyStepCapture.png")

        # Get the width and height of the image
        width, height = screenshot.size

        # Calculate the crop box coordinates
        left = 830
        top = 80
        right = 904
        bottom = 110

        # Crop the image
        cropped_image = screenshot.crop((left, top, right, bottom))

        # Save the cropped image
        cropped_image.save("./img/gotoDifficultyStepCroppedScreenshot.png")
        scanRes = OCRClass.PaddleOCRSingleton.getInstance().scanText('./img/gotoDifficultyStepCroppedScreenshot.png')
        # scanRes = OCRClass.OCRSingleton.getInstance().scanText('./img/gotoDifficultyStepCroppedScreenshot.png')
        print("scanRes: ", scanRes)

        for item in scanRes:
            text = item[0]
            match = re.search(r'關卡(\d+)', text)
            if match:
                number = int(match.group(1))
                print(f"Found number: {number}", "||| DestinationPage(2): ", destinationPage[2],
                      "||| Destination Diff: ",
                      number - destinationPage[2])
                destDiff = number - destinationPage[2]
                if destDiff == 0:
                    print("Found number: ", number)
                    return "ARRIVED"
                else:
                    if destDiff > 0:
                        for i in range(destDiff * 2):
                            ADBClass.AdbSingleton.getInstance().tap((400, 390))
                            time.sleep(0.5)
                    else:
                        return ("error", "difficulty locked")
                    # Check Arrived
                    ADBClass.AdbSingleton.getInstance().screen_capture('./img/gotoDifficultyStepCapture.png')
                    screenshot = Image.open("./img/gotoDifficultyStepCapture.png")

                    # Get the width and height of the image
                    width, height = screenshot.size

                    # Calculate the crop box coordinates
                    left = 830
                    top = 80
                    right = 904
                    bottom = 110

                    # Crop the image
                    cropped_image = screenshot.crop((left, top, right, bottom))

                    # Save the cropped image
                    cropped_image.save("./img/gotoDifficultyStepCroppedScreenshot.png")
                    scanRes = OCRClass.PaddleOCRSingleton.getInstance().scanText(
                        './img/gotoDifficultyStepCroppedScreenshot.png')
                    print("scanRes: ", scanRes)

                    for item in scanRes:
                        text = item[0]
                        match = re.search(r'關卡(\d+)', text)
                        if match:
                            return "ARRIVED"
            else:
                print("No number found.")

    def getMissionListFromConfig(self):
        with open('active_config.yaml', 'r') as file:
            config_data = yaml.safe_load(file)
            return config_data[1]['Material_Mission']['mission'].split(',')

    def startMissionAuto(self, mission_status, mission_code):
        ADBClass.AdbSingleton.getInstance().screen_capture('./img/startMission.png')
        res = OCRClass.OCRSingleton.getInstance().findTextPosition('./img/startMission.png', "代行")
        # res = self.cv2CheckImgExist('./Icons/autoRunMissionBtn.png', './img/startMission.png')
        print("cv2 result (startMission): ", res)
        if res:
            ADBClass.AdbSingleton.getInstance().tap(res[1])
            time.sleep(1)
            ADBClass.AdbSingleton.getInstance().screen_capture('./img/startMission.png')
            res = self.cv2CheckImgExist('./Icons/autoRunMissionBtn.png', './img/startMission.png')
            if res:
                return ("error", "level not avalible for autorun yet")
            cvres = self.cv2CheckImgExist('./Icons/IgnoreInstantAuto.png', './img/startMission.png')
            if cvres is not None:
                with open('active_config.yaml', 'r') as file:
                    config_data = yaml.safe_load(file)
                    # print(config_data[0]['LevelAutomation'][0][mission_code])
                    isFreeAuto = config_data[0]['LevelAutomation'][mission_code]['isFreeAuto']
                    if isFreeAuto:
                        ADBClass.AdbSingleton.getInstance().tap((770, 366))
                        time.sleep(1)
                        ADBClass.AdbSingleton.getInstance().tap((640, 590))
                        return ("success", "free auto")
                    else:
                        ADBClass.AdbSingleton.getInstance().tap(cvres)
                print("cv2 result (startMissionBtn): ", cvres)
                time.sleep(1)
            res = self.clickAutoCharacter(mission_status, mission_code)
            print(res)
            if res[0] is "success":
                ADBClass.AdbSingleton.getInstance().screen_capture('./img/startMission.png')
                cvres = self.cv2CheckImgExist('./Icons/StartAutoBattle.png', './img/startMission.png')
                ADBClass.AdbSingleton.getInstance().tap(cvres)
                print("cv2 result (startMissionBtn): ", cvres)
                time.sleep(3)
                ADBClass.AdbSingleton.getInstance().screen_capture('./img/startMission.png')
                cvres = self.cv2CheckImgExist('./Icons/StartAutoBattle.png', './img/startMission.png')
                if cvres is not None:
                    return ("error", "Some Character Is not avaliable")
                ADBClass.AdbSingleton.getInstance().screen_capture('./img/startMission.png')
                cvres = self.cv2CheckImgExist('./Icons/autoRunMissionCompleted.png', './img/startMission.png')
                if cvres is not None:
                    ADBClass.AdbSingleton.getInstance().tap((640, 660))
            return ("success", res)

    def startMissionFight(self):
        ADBClass.AdbSingleton.getInstance().tap((1050, 630))
        time.sleep(5)
        startMissionFightIsBreak = False
        left = 1120
        top = 510
        right = 1250
        bottom = 600
        for i in range(10):
            ADBClass.AdbSingleton.getInstance().screen_capture('./img/startMission.png')

            scanRes = OctoUtil.OctoUtil.crop_image('./img/startMission.png', (left, top, right, bottom),
                                                   './img/startMissionCroppedScreenshot.png')

            for item in scanRes:
                text = item[0]
                match = text == '開始'
                print("scanResPass: ", text, "||| match: ", match)

                if match:
                    startMissionFightIsBreak = True
                    matchItem = item
                    break
            if startMissionFightIsBreak is True:
                break
            time.sleep(1)
        print("FINAL scanRes: ", scanRes)
        ADBClass.AdbSingleton.getInstance().tap((matchItem[1][0] + left, matchItem[1][1] + top))

        time.sleep(10)

        ADBClass.AdbSingleton.getInstance().screen_capture('./img/startMission.png')
        res = self.cv2CheckImgExist('./Icons/manuelBattleSwitch.png', './img/startMission.png')
        print("cv2 result (startMission): ", res)
        if res:
            ADBClass.AdbSingleton.getInstance().tap(res)

        res = self.cv2CheckImgExist('./Icons/NormalSpeedBattleSwitch.png', './img/startMission.png')
        print("cv2 result (startMission): ", res)
        if res:
            ADBClass.AdbSingleton.getInstance().tap(res)
        # check pixel color in 752,35 is green or not #84ca7c rgba(132,202,124,255)

        time.sleep(2)
        ADBClass.AdbSingleton.getInstance().screen_capture('./img/startMission.png')
        isSpeedAnimation = OctoUtil.OctoUtil.check_pixel_color('./img/startMission.png', 751, 35, (132, 202, 124, 255))
        if isSpeedAnimation is False:
            ADBClass.AdbSingleton.getInstance().tap((752, 35))
        print("isSpeedAnimation: ", isSpeedAnimation)

        fightFinish = False
        while fightFinish is False:
            ADBClass.AdbSingleton.getInstance().screen_capture('./img/inFight.png')
            res = self.cv2CheckImgExist('./Icons/inFightIcon.png', './img/inFight.png')
            print("cv2 result (startMission): ", res)
            if res is None:
                # ADBClass.AdbSingleton.getInstance().tap(res)
                fightFinish = True
                break
            time.sleep(5)
        time.sleep(5)
        ADBClass.AdbSingleton.getInstance().screen_capture('./img/levelUpCheck.png')
        res = self.cv2CheckImgExist('./Icons/levelUpCheck.png', './img/levelUpCheck.png')
        if res:
            ADBClass.AdbSingleton.getInstance().tap((625, 625))
        time.sleep(2)
        ADBClass.AdbSingleton.getInstance().screen_capture('./img/winBattleText.png')
        res = self.cv2CheckImgExist('./Icons/winBattleText.png', './img/winBattleText.png')
        if res:
            ADBClass.AdbSingleton.getInstance().tap(res)
        time.sleep(2)
        ADBClass.AdbSingleton.getInstance().screen_capture('./img/winFightMaterialScreen.png')
        res = self.cv2CheckImgExist('./Icons/winFightMaterialScreen.png', './img/winFightMaterialScreen.png')
        if res:
            ADBClass.AdbSingleton.getInstance().tap(res)
        time.sleep(2)
        return ("clickAutoCharacter")

    def mapMissionToStatus(self, index, input):
        # should upgrade to {"DailyMaterial" : ["EXP", "MON", "WEA", "SRD"], ...}
        # "EXP": Expereince, "MON": Money, "WUP": Weapon Upgrade, "WEA": Weapon, "SRD": Shard
        auto_dictionary = ["EXP", "WUP", "ENC", "STAR", "WEA", "SRD", "TRT"]
        manual_dictionary = []

        single_level_dictionary = ["EXP", "WUP", "SRD"]
        multi_level_dictionary = ["STAR", "ENC", "WEA", "TRT"]
        for key in auto_dictionary:
            if key in input:
                prefix = key
                suffix = input.replace(key, "")
                if OctoUtil.OctoUtil.check_string(suffix) is True:
                    full_suffix = suffix.split("_")
                    levelNo = full_suffix[0]
                    levelNo = OctoUtil.OctoUtil.map_char_num(levelNo)
                    suffix = int(full_suffix[1])
                else:
                    suffix = int(suffix.lstrip("_"))
                    levelNo = None
                with open('active_config.yaml', 'r') as file:
                    config_data = yaml.safe_load(file)
                    if config_data[0]['LevelAutomation'][list(config_data[0]['LevelAutomation'].keys())[index]][
                        'isAuto'] is True:
                        category = "DailyMaterialAuto"
                    else:
                        category = "DailyMaterialFight"
        # for key in manual_dictionary:
        #     if key in input:
        #         prefix = key
        #         suffix = input.replace(key, "")
        #         if OctoUtil.OctoUtil.check_string(suffix) is True:
        #             full_suffix = suffix.split("_")
        #             levelNo = full_suffix[0]
        #             levelNo = OctoUtil.OctoUtil.map_char_num(levelNo)
        #             suffix = int(full_suffix[1])
        #         else:
        #             suffix = int(suffix.lstrip("_"))
        #             levelNo = None
        #         category = "DailyMaterialFight"

        for key in single_level_dictionary:
            if key in input:
                levelType = "single"

        for key in multi_level_dictionary:
            if key in input:
                levelType = "multi"

        return category, prefix, suffix, levelType, levelNo
    def run(self):
        adb_is_connected = ADBClass.AdbSingleton.getInstance().connectDevice(adb_path=self.adb_path, adb_port=self.adb_port,
                                                                retryCount=20)

        missionList = self.getMissionListFromConfig()
        with open('active_config.yaml', 'r') as file:
            config_data = yaml.safe_load(file)
            missionActiveNameList = list(config_data[0]['LevelAutomation'].keys())
        for index, mission in enumerate(missionList):
            missionActiveName = missionActiveNameList[index]
            missionStatus = self.mapMissionToStatus(index, mission)
            print("mission status: ", missionStatus)
            det_res = self.checkCurrentPageStatus(missionStatus)
            while det_res[0] != "ARRIVED":
                det_res = self.checkCurrentPageStatus(missionStatus)
                print("det_res", det_res)
                GotoStepRes = self.GotoDailyMaterialStep(det_res, missionStatus)
                print("GotoStepRes", GotoStepRes)
                if GotoStepRes == "ARRIVED":
                    time.sleep(2)
                    break
                time.sleep(2)
            GotoMiddleRes = self.GotoMiddleStep(missionStatus)
            GotoDifficultyRes = self.GotoDifficultyStep(missionStatus)
            if GotoDifficultyRes == "ARRIVED":
                print("GotoDifficultyRes ARRIVED")
                time.sleep(2)
                if missionStatus[0] == "DailyMaterialAuto":
                    startMissionRes = self.startMissionAuto(missionStatus, missionActiveName)
                elif missionStatus[0] == "DailyMaterialFight":
                    startMissionRes = self.startMissionFight()
        # ADBClass.AdbSingleton.getInstance().screen_capture("loginCapture.png")

        return input