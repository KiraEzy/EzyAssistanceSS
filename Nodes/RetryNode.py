import time

import numpy as np
from BaseNode import BaseNode

class RetryNode(BaseNode):
    def __init__(self, parentFlow , nodeName, parentNode, nextNode, actionFunction, isRootNode,verificationFunction ,targetValue, retryCount, retryInterval: float = 0.5):
        self.targetValue = targetValue
        self.retryCount = retryCount
        self.verificationFunction = verificationFunction
        self.retryInterval = retryInterval
        super().__init__(parentFlow ,nodeName, parentNode, nextNode, actionFunction, isRootNode)


    def executeAction(self):
        res = super().executeAction()
        while self.verificationFunction(res) != self.targetValue:
            self.retryCount -= 1
            res = super().executeAction()
            if self.retryCount == 0:
                break
            time.sleep(self.retryInterval)
        if self.retryCount == 0:
            return {"error" : "Retry count exceeded"}
        else:
            return res