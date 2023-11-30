import unittest
from BaseFlow import BaseFlow
from BaseNode import BaseNode
from DeciderNode import DeciderNode


class TestBaseFlow(unittest.TestCase):
    def test_execute_flow(self):
        # Create a flow with a BaseNode and a DeciderNode
        def multiply_by_two(inputObj):
            return {"number": inputObj["number"] * 2}
        def divide_by_two(inputObj):
            return {"number": inputObj["number"] / 2}
        def deciderNodeFunction(x):
            return [{"number": x},"True"] if x > 10 else [{"number": x},"False"]
        node1 = BaseNode("Node1", None, None, multiply_by_two, False)
        node3 = BaseNode("Node3", None, None, divide_by_two, False)
        node2 = DeciderNode(nodeName="Node2", parentNode=None, nextNode=None, actionFunction=deciderNodeFunction,isRootNode= False,returnMapper= {"True": node1, "False": node3})
        node1_2 = BaseNode("Node1_2", None, None, multiply_by_two, False)
        node3_2 = BaseNode("Node3_2", None, None, divide_by_two, False)
        node1.setNextNode(node1_2)
        node3.setNextNode(node3_2)
        flow = BaseFlow(node2)

        # Execute the flow with inputVar = 8
        # Check if the result is as expected
        self.assertEqual(flow.executeFlow(8), {"number": 2})
        # Check if the flow history is as expected
        self.assertEqual(flow.FlowHistory, ["Node2", "Node3", "Node3_2"])
        flow2 = BaseFlow(node2)

        # Execute the flow with inputVar = 12
        # Check if the result is as expected
        self.assertEqual(flow2.executeFlow(12), {"number": 48})
        # Check if the flow history is as expected
        self.assertEqual(flow2.FlowHistory, ["Node2", "Node1", "Node1_2"])


if __name__ == '__main__':
    unittest.main()