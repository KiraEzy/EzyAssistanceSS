import os
import re

import cv2
import numpy as np
import yaml
from PIL import Image

import ADBClass
import OCRClass


class OctoUtil:
    @staticmethod
    def detectImgOCR(m_ocr, img_path):
        # img_path = os.path.join('.', 'img', 'screenshot.png')
        result = m_ocr.ocr(img_path, cls=True)
        print("res: ", result[0])

        return result
    @staticmethod
    def check_hv_certain_word(m_ocr, target,profile):
        profile.screen_capture("./img/screenshot.png")
        resultArr = OctoUtil.detectImgOCR(m_ocr, "./img/screenshot.png")
        passedData = []
        #print(resultArr, target)
        for line in resultArr[0]:
            if (OctoUtil.check_percent(line[1][0], target, 0.7)[0] is True):
                passedData.append((line[1][0], (OctoUtil.check_percent(line[1][0], target, 0.7)[1]), line[0]))
                print("text: ", line[1][0], " confidence: ", line[1][1], " rect: ", line[0], "checkRes: ",
                    OctoUtil.check_percent(line[1][0], target, 0.7))
        #print("return: ", len(passedData) > 0)
        max_item = ()
        if len(passedData) > 0:
            max_item = max(passedData, key=lambda x: x[1])
            print("MaxItem: ", max_item, np.mean(np.array(max_item[2]), axis=0))
            return [len(passedData) > 0, np.mean(np.array(max_item[2]), axis=0)]
        else:
            return [len(passedData) > 0, ()]

    @staticmethod
    def print_param(params):
        print(params)

    @staticmethod
    def check_percent(main_text, verification_text, percent_overlap_text_appearance_in_verification_text):
        words_main_text = OctoUtil.split_str(main_text)
        words_verification_text = OctoUtil.split_str(verification_text)
        count = 0
        for word in words_main_text:
            if word in words_verification_text:
                #print(word)
                count += 1
        overlap_text_appearance_in_verification_text = count / len(words_verification_text) * 100
        verification_text_perc_in_main_text = len(words_verification_text) / len(words_main_text) * 100
        #print(main_text, verification_text, overlap_text_appearance_in_verification_text, verification_text_perc_in_main_text)
        return overlap_text_appearance_in_verification_text >= percent_overlap_text_appearance_in_verification_text, verification_text_perc_in_main_text

    # @staticmethod
    # def check_pixel_color(img_path, pixel_coord, target_color, profile, return_value): #eg:"./screenshot.png", (100,100), [255,0,0]
    #     profile.screen_capture(img_path)
    #     # Open the image file
    #     image = Image.open(img_path)
    #
    #     # Get the color of a specific pixel
    #     pixel_color = image.getpixel(pixel_coord)  # Replace with the x and y coordinates of the desired pixel
    #
    #     # Print the color values
    #     print("Color(RGB): ", pixel_color, len(return_value))
    #     if(len(return_value) == 0):
    #         return pixel_color == tuple(target_color[0])
    #     elif(len(return_value) == len(target_color)):
    #         for i in range(len(target_color)):
    #             color = target_color[i]
    #             if pixel_color == tuple(color):
    #                 return return_value[i]
    #         return "err"
    #     elif (len(return_value)-1 == len(target_color)):
    #         for i in range(len(target_color)):
    #             color = target_color[i]
    #             if pixel_color == tuple(color):
    #                 return return_value[i]
    #         return return_value[len(return_value)-1]

    @staticmethod
    def check_pixel_color(image_path, coordinate_x, coordinate_y, color):
        image = Image.open(image_path)
        # Get the color of a specific pixel
        pixel_color = image.getpixel((coordinate_x, coordinate_y))  # Replace with the x and y coordinates of the desired pixel
        print("Color(RGB): ", pixel_color)
        return pixel_color == color

    @staticmethod
    def pad_number_with_zeros(string, number):
        return f"{string}_{number:02d}"

    @staticmethod
    def split_str(text):
        chars = []
        for c in text:
            chars.append(c)
        return chars

    @staticmethod
    def crop_image(screenshot_path, lrtb, cropped_path):
        screenshot = Image.open(screenshot_path)
        cropped_image = screenshot.crop(lrtb)

        # Save the cropped image
        cropped_image.save(cropped_path)
        scanRes = OCRClass.OCRSingleton.getInstance().scanText(cropped_path)
        return scanRes
    @staticmethod
    def check_string(string):
        pattern = re.compile(r'[A-Za-z]')
        match = pattern.search(string)
        return bool(match)

    @staticmethod
    def map_char_num(letter):
        return ord(letter) - ord('A') + 1

    @staticmethod
    def eliminate_close_values(array, threshold):
        result = []
        for value in array:
            if all(abs(value - other) > threshold for other in result):
                result.append(value)
        return result
    @staticmethod
    def parse_mission_to_yaml(mission):
        with open('active_config.yaml', 'w', encoding='utf-8') as configfile:

            # data = [
                # {'LevelAutomation': [{'EXP_07': {'characters': '澤維爾,迪塔利奧'} }]},
            # ]
            data = [
                {'LevelAutomation': {}},
                {'Material_Mission': {'mission': ""}}
            ]
            missionListStr = ""
            for level in mission:
                charList = ""
                for char in level.characterList:
                    charList += char
                    charList += ","
                if len(charList) > 0:
                    charList = charList[:-1]
                midMissionChar = ""
                if level.midMission is not None:
                    midMissionChar = level.midMission
                missionListStr += OctoUtil.pad_number_with_zeros(level.missionId + midMissionChar, level.difficulty)
                missionListStr += ","

                data[0]['LevelAutomation'][OctoUtil.pad_number_with_zeros(level.missionId + midMissionChar, level.difficulty)] = {
                    'characters': charList,
                    'isAuto': level.auto,
                    'isFreeAuto': level.freeAuto
                }

            # Write the list of dictionaries to a YAML file
            if len(missionListStr) > 0:
                missionListStr = missionListStr[:-1]
                data[1]['Material_Mission']['mission']+=str(missionListStr)
            with open('active_config.yaml', 'w') as file:
                yaml.dump(data, file)

    @staticmethod
    def checkSelectedCharNum(top, left, bottom, right, inputImgPath = None):
        ADBClass.AdbSingleton().getInstance().connectDevice("D:\\mumu2\\emulator\\nemu\\vmonitor\\bin\\adb_server.exe",
                                              "127.0.0.1:7555")
        if inputImgPath is None:
            inputImgPath = './img/checkSelectedCharNum.png'
            ADBClass.AdbSingleton.getInstance().screen_capture(inputImgPath)
        screenshot = Image.open(inputImgPath)
        cropped_image = screenshot.crop((left, top, right, bottom))

        dir_name = os.path.dirname(inputImgPath)
        file_name, extension = os.path.splitext(os.path.basename(inputImgPath))

        # Append the additional text and reconstruct the new path
        new_file_name = file_name + 'CroppedScreenshot' + extension
        croppedInputImgPath = os.path.join(dir_name, new_file_name)

        cropped_image.save(croppedInputImgPath)
        res = OCRClass.OCRSingleton.getInstance().scanText(croppedInputImgPath)
        print(res)
        return res

    @staticmethod
    def parse_mission_to_preset_yaml(mission, fileName):
        with open(fileName, 'w', encoding='utf-8') as configfile:

            # data = [
            # {'LevelAutomation': [{'EXP_07': {'characters': '澤維爾,迪塔利奧'} }]},
            # ]
            data = [
                {'LevelAutomation': {}},
                {'Material_Mission': {'mission': ""}}
            ]
            missionListStr = ""

            for level in mission:
                charList = ""
                for char in level.characterList:
                    charList += char
                    charList += ","
                if len(charList) > 0:
                    charList = charList[:-1]
                midMissionChar = ""
                if level.midMission is not None:
                    midMissionChar = level.midMission
                missionListStr += OctoUtil.pad_number_with_zeros(level.missionId + midMissionChar, level.difficulty)
                missionListStr += ","

                if(not OctoUtil.pad_number_with_zeros(level.missionId + midMissionChar, level.difficulty) in list(data[0]['LevelAutomation'].keys())):
                    data[0]['LevelAutomation'][
                        OctoUtil.pad_number_with_zeros(level.missionId + midMissionChar, level.difficulty)] = {
                        'characters': charList,
                        'isAuto': level.auto,
                        'isFreeAuto': level.freeAuto
                    }
                else:
                    itrCounter = 1
                    while (OctoUtil.pad_number_with_zeros(level.missionId + midMissionChar, level.difficulty) + "_" + str(itrCounter) in list(data[0]['LevelAutomation'].keys())):
                        itrCounter += 1

                    data[0]['LevelAutomation'][
                        OctoUtil.pad_number_with_zeros(level.missionId + midMissionChar, level.difficulty) + "_" + str(itrCounter)] = {
                        'characters': charList,
                        'isAuto': level.auto,
                        'isFreeAuto': level.freeAuto
                    }

            # Write the list of dictionaries to a YAML file
            if len(missionListStr) > 0:
                missionListStr = missionListStr[:-1]
                data[1]['Material_Mission']['mission'] += str(missionListStr)
            with open(fileName, 'w') as file:
                yaml.dump(data, file)