
# File: BinaryTree.py
# Author(s): Jordan Giebas

class BinaryTree:
    class _BTNode:
        def __init__(self, value, left = None, right = None):
            self._value = value
            self._left = left
            self._right = right
    def __init__(self):
        self._top = None
    def insert(self, value):
        if self._top == None:
            self._top = self._BTNode(value)
        else:
            ... yours to finish ...



# test code:

bt = BinaryTree()
print(bt)
print(bt.size())
print(bt.depth())
bt.insert(7)
bt.insert(3)
bt.insert(2)
bt.insert(13)
bt.insert(9)
bt.insert(3)
print(bt)
print(bt.size())
print(bt.depth())
bt.print_pretty()
