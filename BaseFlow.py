from BaseNode import BaseNode
from DeciderNode import DeciderNode

class BaseFlow:
    def __init__(self, node: BaseNode):
        self.rootNode = node
        self.FlowHistory = []
        self.NodeList = []
        self.currentNode = self.rootNode
        self.skipTargetNode = None
        self.isSkipping = False
    def traverseFlow(self):
        if not self.rootNode:
            raise ValueError('No root node set for flow')
        else:
            self.rootNode.setRootNode(True)
            self.currentNode = self.rootNode
            print("#######################", "Flow Start Root Node: ", self.rootNode.nodeName, " | Parameter:  ", self.rootNode.parameter,
                  "#######################")
            while self.currentNode:
                nextNode = self.currentNode.nextNode
                self.FlowHistory.append(self.currentNode.nodeName)
                if isinstance(self.currentNode, DeciderNode): # Decider Node
                    DeciderCurrentNode = self.currentNode # type: DeciderNode
                    DeciderCurrentNode.executeAction() #  type: # where [result , mapper] is a list
                    nextNode : BaseNode = DeciderCurrentNode.getMappedNextNode(DeciderCurrentNode.fullRes[1]) # get Mapped Next Node type: BaseNode
                    print('Decider NodeMapper Varible: ', DeciderCurrentNode.fullRes[1])
                    self.currentNode.nextNode = nextNode
                    if self.isSkipping:
                        self.isSkipping = False
                        nextNode = self.skipTargetNode
                        self.skipTargetNode = None
                        print('Decider Node Skipping to: ', nextNode.nodeName)
                    else:
                        nextNode.parentNode = self.currentNode # type: BaseNode
                        nextNode.parameter = DeciderCurrentNode.fullRes[0]
                    print('Decider Next Node: ', nextNode.nodeName)
                else:
                    res = self.currentNode.executeAction()
                    if "error" in res:
                        print("Error in node: ", self.currentNode.nodeName, " | Error: ", res["error"])
                        return res
                    if self.isSkipping:
                        self.isSkipping = False
                        nextNode = self.skipTargetNode
                        self.skipTargetNode = None
                        print('Decider Node Skipping to: ', nextNode.nodeName)
                    if nextNode:
                        print('Next Node', nextNode.nodeName)
                    else:
                        print('No Next Node')


                if nextNode:
                    self.currentNode = nextNode
                else:
                    self.currentNode = None
                    return res

    def appendToNodeList(self, node: BaseNode):
        self.NodeList.append(node)

    def executeFlow(self, inputVar=None):
        if inputVar is not None:
            self.rootNode.parameter = inputVar
        res = self.traverseFlow()
        return res

    def skipToNode(self, nodeName, parameter=None):
        for node in self.NodeList:
            if node.nodeName == nodeName:

                if parameter is not None:
                    node.parameter = parameter
                else:
                    node.parameter = self.currentNode.parameter
                self.skipTargetNode = node
                self.isSkipping = True
                break
        return self.currentNode