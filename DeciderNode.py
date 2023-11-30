import BaseNode


class DeciderNode(BaseNode.BaseNode):
    def __init__(self, nodeName, parentNode, nextNode, actionFunction, isRootNode, returnMapper):
        super().__init__(nodeName, parentNode, nextNode, actionFunction, isRootNode)
        self.returnMapper = returnMapper;

        # Add any additional properties or initialize them as needed

    def getMappedNextNode(self, input_key):
        return self.returnMapper[input_key];
        # Add additional methods specific to the extended node

    # Override any methods from the base class if necessary