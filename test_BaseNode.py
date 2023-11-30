import unittest
from BaseNode import BaseNode


class TestBaseNode(unittest.TestCase):
    def test_new_node(self):
        # Create a new instance of BaseNode with desired parameters
        node = BaseNode("NewNode", None, None, lambda x: x * 2, 5, False)

        # Invoke the executeAction method
        result = node.executeAction()

        # Check if the result is as expected
        self.assertEqual(result, 10)


if __name__ == '__main__':
    unittest.main()