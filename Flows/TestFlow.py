import copy
import sys

from BaseFlow import BaseFlow
from BaseNode import BaseNode
from DeciderNode import DeciderNode
from Nodes.ADBNodes import SetupADBNode, StartAppNode, ScreenShotNode, cvMatchScreenshotNode, ClickNode, \
    tapUntilMatchFixedPos, DailyMaterialNode, LoginRewardNode
from Nodes.GeneralNodes import WaitSecondsNode, cvMatchTemplateNode
class StartAppFlow(BaseFlow):
    def __init__(self, adbPath, adbPort, retryCount):
        self.setup_adb_node = SetupADBNode(self,"SetupADBNode", None, None, True)
        super().__init__(self.setup_adb_node)
        self.rootNode = self.setup_adb_node
        self.rootNode.parameter = {"adb_path": adbPath, "adb_port": adbPort, "retry_count": retryCount}
        self.start_app_node = StartAppNode(self,"StartAppNode", self.setup_adb_node, None, False)
        self.sleep_node = WaitSecondsNode(self,"SleepNode", self.start_app_node, None, False, 5)
        # self.screen_shot_node_login = ScreenShotNode("ScreenShotNode_login", self.sleep_node, None, False, "./img/loginCapture.png")
        self.cv_match_template_node_login = cvMatchScreenshotNode(self, "cvMatchTemplateNode_login", self.sleep_node,
                                                                  None, False, "./img/loginCapture.png", "./Icons/loginBulletinClose.png",
                                                                  15, 5,
                                                                  [
                                                                      {
                                                                          "subPattern": "./Icons/loginStartGame.png",
                                                                          "function": self.skipToNode,
                                                                          "parameters": "cv_login_click_node_login"
                                                                      },
                                                                      {
                                                                          "subPattern": "./Icons/loggedInCheckImg.png",
                                                                          "function": self.skipToNode,
                                                                          "parameters": "FinalSleepNode"
                                                                      }
                                                                  ]
                                                                  )
        self.clickLoginBulletinCloseNode = ClickNode(self,"ClickLoginBulletinCloseNode", self.cv_match_template_node_login, None, False)
        self.cv_login_click_node_login = cvMatchScreenshotNode(self,"cv_login_click_node_login", self.clickLoginBulletinCloseNode, None, False,
                                                               "./img/loginButtonCapture.png", "./Icons/loginStartGame.png", 15, 5,
                                                               [
                                                                   {
                                                                       "subPattern": "./Icons/loggedInCheckImg.png",
                                                                       "function": self.skipToNode,
                                                                       "parameters": "FinalSleepNode"
                                                                   }
                                                               ]
                                                               )
        self.clickLoginButtoninCloseNode = ClickNode(self,"ClickLoginButtonCloseNode_login", self.cv_login_click_node_login,None, False)
        self.dailyRewardNode = LoginRewardNode(self,"ClickRewardNode", self.clickLoginButtoninCloseNode, None, False)
        self.finalSleepNode = WaitSecondsNode(self, "FinalSleepNode", self.dailyRewardNode, None, False, 1)

        self.setup_adb_node.setNextNode(self.start_app_node)
        self.setup_adb_node.setNextNode(self.start_app_node)
        self.start_app_node.setNextNode(self.sleep_node)
        self.sleep_node.setNextNode(self.cv_match_template_node_login)
        self.cv_match_template_node_login.setNextNode(self.clickLoginBulletinCloseNode)
        self.clickLoginBulletinCloseNode.setNextNode(self.cv_login_click_node_login)
        self.cv_login_click_node_login.setNextNode(self.clickLoginButtoninCloseNode)
        self.clickLoginButtoninCloseNode.setNextNode(self.dailyRewardNode)
        self.dailyRewardNode.setNextNode(self.finalSleepNode)

        self.appendToNodeList(self.setup_adb_node)
        self.appendToNodeList(self.start_app_node)
        self.appendToNodeList(self.sleep_node)
        self.appendToNodeList(self.cv_match_template_node_login)
        self.appendToNodeList(self.clickLoginBulletinCloseNode)
        self.appendToNodeList(self.cv_login_click_node_login)
        self.appendToNodeList(self.clickLoginButtoninCloseNode)
        self.appendToNodeList(self.dailyRewardNode)
        self.appendToNodeList(self.finalSleepNode)

class DailyMaterialFlow(BaseFlow):
    def __init__(self, adbPath, adbPort, retryCount):
        self.setup_adb_node = SetupADBNode(self,"SetupADBNode", None, None, True)
        super().__init__(self.setup_adb_node)
        self.rootNode = self.setup_adb_node
        self.rootNode.parameter = {"adb_path": adbPath, "adb_port": adbPort, "retry_count": retryCount}

        self.runMaterialFlow = DailyMaterialNode(self,"DailyMaterialNode", self.setup_adb_node, None, False)
        self.sleep_node = WaitSecondsNode(self,"SleepNode", self.runMaterialFlow, None, False, 5)

        self.setup_adb_node.setNextNode(self.runMaterialFlow)
        self.runMaterialFlow.setNextNode(self.sleep_node)

        self.appendToNodeList(self.setup_adb_node)
        self.appendToNodeList(self.runMaterialFlow)
        self.appendToNodeList(self.sleep_node)



class TestFlowOcto(BaseFlow):
    def __init__(self, adbPath, adbPort, retryCount):
        self.setup_adb_node = SetupADBNode(self,"SetupADBNode", None, None, True)
        super().__init__(self.setup_adb_node)
        self.rootNode = self.setup_adb_node
        self.rootNode.parameter = {"adb_path": adbPath, "adb_port": adbPort, "retry_count": retryCount}
        self.start_app_node = StartAppNode(self,"StartAppNode", self.setup_adb_node, None, False)

        self.sleep_node = WaitSecondsNode(self,"SleepNode", self.start_app_node, None, False, 10)
        self.tap_until_match_login = tapUntilMatchFixedPos(self,"tapUntilMatch_login", self.sleep_node, None, False, "./img/loginCapture.png", "./Icons/OctoMenuBtn.png", (500,500))

        self.setup_adb_node.setNextNode(self.start_app_node)
        self.start_app_node.setNextNode(self.sleep_node)
        self.sleep_node.setNextNode(self.tap_until_match_login)
        # self.screen_shot_node_login.setNextNode(self.cv_match_template_node_login)
