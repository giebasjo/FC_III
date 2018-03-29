# File: BinaryTree.py
# Author(s): Lucas Duarte Bahia
#            Jordan Giebas
#            Harveen Oberoi
#            Daniel Rojas Coy

class BinaryTree:

    class _BTNode:
        def __init__(self, value, left = None, right = None):
            self._value = value
            self._left = left
            self._right = right

    def __init__(self):
        self._top  = None
        self._list = list()

    def insert(self, value, node = None):

        if self._top == None:
            self._top = self._BTNode(value)
            self._list.append( str(value) )
        elif node==None:
            if value < self._top._value:
                if self._top._left == None:
                    self._top._left = self._BTNode(value)
                    self._list.append( str(value) )
                else:
                    # self._top = self._top._left
                    self.insert(value, self._top._left)
            elif value > self._top._value:
                if self._top._right == None:
                    self._top._right = self._BTNode(value)
                    self._list.append( str(value) )
                else:
                    # self._top = self._top._right
                    self.insert(value, self._top._right)
        else:
            if value < node._value:
                if node._left == None:
                    node._left = self._BTNode(value)
                    self._list.append( str(value) )
                else:
                    # self._top = self._top._left
                    self.insert(value, node._left)
            elif value > node._value:
                if node._right == None:
                    node._right = self._BTNode(value)
                    self._list.append( str(value) )
                else:
                    # self._top = self._top._right
                    self.insert(value, node._right)


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

    def print_pretty(self):

        def pp_helper(node, level):
            if node is None:
                return
            pp_helper(node._right, level+1)
            tmp_str = ""
            for i in range(level):
                tmp_str += "\t"
            print(tmp_str + str(node._value))

            pp_helper(node._left, level+1)


        if self._top == None:
            return

        pp_helper(self._top, 0)

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
bt.insert(3) # ignores since duplicate
print("--done inserting--")
print("Printing Binary Tree: ", bt)
print("Tree Size: ", bt.size())
print("Tree Depth: ", bt.depth())
print("Printing pretty --- ")
bt.print_pretty()