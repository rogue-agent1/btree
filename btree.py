#!/usr/bin/env python3
"""btree - B-tree with insert, search, and ordered traversal."""
import sys

class BTreeNode:
    def __init__(self, t, leaf=True):
        self.t = t
        self.keys = []
        self.children = []
        self.leaf = leaf

class BTree:
    def __init__(self, t=3):
        self.t = t
        self.root = BTreeNode(t)
    def search(self, key, node=None):
        if node is None:
            node = self.root
        i = 0
        while i < len(node.keys) and key > node.keys[i]:
            i += 1
        if i < len(node.keys) and key == node.keys[i]:
            return True
        if node.leaf:
            return False
        return self.search(key, node.children[i])
    def insert(self, key):
        root = self.root
        if len(root.keys) == 2 * self.t - 1:
            new_root = BTreeNode(self.t, leaf=False)
            new_root.children.append(self.root)
            self._split(new_root, 0)
            self.root = new_root
        self._insert_nonfull(self.root, key)
    def _insert_nonfull(self, node, key):
        i = len(node.keys) - 1
        if node.leaf:
            node.keys.append(None)
            while i >= 0 and key < node.keys[i]:
                node.keys[i + 1] = node.keys[i]
                i -= 1
            node.keys[i + 1] = key
        else:
            while i >= 0 and key < node.keys[i]:
                i -= 1
            i += 1
            if len(node.children[i].keys) == 2 * self.t - 1:
                self._split(node, i)
                if key > node.keys[i]:
                    i += 1
            self._insert_nonfull(node.children[i], key)
    def _split(self, parent, i):
        t = self.t
        child = parent.children[i]
        new_node = BTreeNode(t, leaf=child.leaf)
        parent.keys.insert(i, child.keys[t - 1])
        parent.children.insert(i + 1, new_node)
        new_node.keys = child.keys[t:]
        child.keys = child.keys[:t - 1]
        if not child.leaf:
            new_node.children = child.children[t:]
            child.children = child.children[:t]
    def inorder(self, node=None):
        if node is None:
            node = self.root
        result = []
        for i in range(len(node.keys)):
            if not node.leaf:
                result.extend(self.inorder(node.children[i]))
            result.append(node.keys[i])
        if not node.leaf:
            result.extend(self.inorder(node.children[-1]))
        return result

def test():
    bt = BTree(t=2)
    for x in [10, 20, 5, 6, 12, 30, 7, 17]:
        bt.insert(x)
    assert bt.inorder() == [5, 6, 7, 10, 12, 17, 20, 30]
    assert bt.search(12) and bt.search(30)
    assert not bt.search(99) and not bt.search(0)
    bt2 = BTree(t=3)
    for x in range(100):
        bt2.insert(x)
    assert bt2.inorder() == list(range(100))
    assert bt2.search(50) and not bt2.search(100)
    print("OK: btree")

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "test":
        test()
    else:
        print("Usage: btree.py test")
