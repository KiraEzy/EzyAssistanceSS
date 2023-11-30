import time

import cv2

from BaseNode import BaseNode
from Nodes.RetryNode import RetryNode
import ADBClass
import numpy as np
from OctoUtil import OctoUtil

class WaitSecondsNode(BaseNode):
    def node_wait_seconds(self, input={}):
        time.sleep(self.second)
        return input

    def __init__(self,parentFlow, nodeName, parentNode, nextNode, isRootNode, seconds):
        inputFunc = self.node_wait_seconds
        super().__init__(parentFlow,nodeName, parentNode, nextNode, inputFunc, isRootNode)
        self.second = seconds

class cvMatchTemplateNode(RetryNode):
    def node_cv_match_template(self, input={}):
        print("node_cv_match_template",self.pattern, input["cv2_img_screenshot"])
        screenshot = cv2.imread(input["cv2_img_screenshot"], 0)
        pattern = cv2.imread(self.pattern, 0)
        result = cv2.matchTemplate(pattern, screenshot, cv2.TM_CCOEFF_NORMED)
        threshold = 0.8

        # Find the location of matched regions above the threshold
        locations = np.where(result >= threshold)

        # Draw rectangles around the matched regions
        for pt in zip(*locations[::-1]):
            cv2.rectangle(screenshot, pt, (pt[0] + pattern.shape[1], pt[1] + pattern.shape[0]), (0, 255, 0), 2)

        # Display the result
        cv2.imshow('Result', screenshot)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

        if len(locations[0]) > 0:
            print("There is a result.")
        else:
            print("There is no result.")
            # try subPattern cv, if res is not empty, set output to subpattern related result, then skip to the desired
            # node, where subpatterns should be key value pair, key is the subpattern, value is the result action, then
            # breaks the retry by returning True in the verification function
            # SAMPLE:
            # subPattern = {
            #     "subPattern": "./sample.png",
            #     "function": "myFunc",
            #     "parameters": {
            #         "paramA": "A",
            #         "paramB": 125
            #     }
            # }
            if self.subPattern is not None:
                for subPattern in self.subPattern:
                    subPatternResult = cv2.matchTemplate(subPattern["subPattern"], screenshot, cv2.TM_CCOEFF_NORMED)
                    subPatternThreshold = 0.8
                    subPatternLocations = np.where(subPatternResult >= subPatternThreshold)
                    if len(subPatternLocations[0]) > 0:
                        print("There is a sub pattern result.")
                        subPattern["function"](subPattern["parameters"])
                        return input

        # size_1 = locations[0][0]  # Extracts the first element of the first array
        # size_2 = locations[1][0]  # Extracts the first element of the second array
        #
        # print(size_1)  # Output: 113
        # print(size_2)  # Output: 1030
        input["cv2_img_screenshot_result"] = locations
        return input
    def verify_cv_result(self, verifyInput):
        return len( verifyInput["cv2_img_screenshot_result"][0]) > 0
    def __init__(self,parentFlow, nodeName, parentNode, nextNode, isRootNode, pattern, retryCount, retryInterval = 1, subPattern = None):
        inputFunc = self.node_cv_match_template
        super().__init__(parentFlow,nodeName, parentNode, nextNode, inputFunc, isRootNode, self.verify_cv_result, True, retryCount, retryInterval)
        self.pattern = pattern
        self.subPattern = subPattern
