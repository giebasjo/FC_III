
# File: BinaryTree.py
# Author(s): Jordan Giebas

class BinaryTree:

    class _BTNode:
        def __init__(self, value, left = None, right = None):
            self._value = value
            self._left = left
            self._right = right

    def __init__(self):
        self._top  = None
        self._list = list()

    def insert(self, value):

        if self._top == None:
            self._top = self._BTNode(value)
            self._list.append( str(value) )
        else:
            if value < self._top._value:
                if self._top._left == None:
                    self._top._left = self._BTNode(value)
                    self._list.append( str(value) )
                else:
                    self._top = self._top._left
                    self.insert(value)
            elif value > self._top._value:
                if self._top._right == None:
                    self._top._right == self._BTNode(value)
                    self._list.append( str(value) )
                else:
                    self._top = self._top._right
                    self.insert(value)

    def __str__(self):
        return " ".join(self._list)

    def size(self):
        return len(self._list)

    def depth(self):

        def depth_helper(node):
            if node is None:
                return 0
            else:
                l_depth = depth_helper(node._left)
                r_depth = depth_helper(node._right)
            return max(l_depth, r_depth) + 1

        return depth_helper(self._top)

    def print_pretty_helper(self, node, level):

        if self._top == None:
            return ""
        
        self.print_pretty_helper(self._top._right, level + 1)
        for i in range(level):
            print('\t')
        
        print(self._top._value)
        self.print_pretty_helper(self._top._left, level + 1)

    def print_pretty(self):

        if self._top == None:
            return ""

        self.print_pretty_helper(self._top,0)


# test code:
bt = BinaryTree()
print("Printing Binary Tree: ", bt)
print("Size: ", bt.size())
print("Depth: ", bt.depth())
print("--inserting--")
bt.insert(7)
bt.insert(3)
bt.insert(2)
bt.insert(13)
bt.insert(9)
bt.insert(3)
print("--done inserting--")
print("Printing Binary Tree: ", bt)
print("Tree Size: ", bt.size())
print("Tree Depth: ", bt.depth())
#print("Printing pretty --- ")
#bt.print_pretty()


