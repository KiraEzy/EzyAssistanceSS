# import * as fs from 'fs';

import numpy as np


class BaseNode:
    def __init__(self, parentFlow, nodeName, parentNode, nextNode, actionFunction, isRootNode):
        self.parentFlow = parentFlow
        self.nodeName = nodeName
        self.parentNode = parentNode
        self.nextNode = nextNode
        self.actionFunction = actionFunction
        self.parameter = None
        self.isRootNode = isRootNode
        self.fullRes = {}
        #writeDataFile(nodeName, {})

    def setRootNode(self, isRootNode: bool):
        self.isRootNode = isRootNode;


    def setParentNode(self, node):
        self.parentNode = node;
        node.nextNode = self;


    def setNextNode(self, node):
        self.nextNode = node;
        node.parentNode = self;

    def setParameter(self, parameter):
        self.parameter = parameter;

    def executeAction(self):
        currentNode = self;
        result = None;
        #if (self.parameter != None):
        print("-----------------------", "Node Name: ", currentNode.nodeName, " | Parameter:  " , self.parameter, "(Length:", len(self.parameter) ,")", "-----------------------")
        result = self.actionFunction(self.parameter);
        print("Node actionFunction Result: ", result)
        self.fullRes = result;
        if (isinstance(result, (list, tuple, np.ndarray))):
            load = result[0];
            print("Decider Node Load", load," | Decider Node resultMapper: ", result[1])
        else:
            load = result;
        if (self.nextNode != None):
            self.nextNode.parameter = load;
            print("Node Load", load)
        return load;
        #writeDataFile(this.nodeName, load)
