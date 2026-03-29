#!/usr/bin/env python3
"""B-tree implementation with insert, search, delete, and visualization."""
import sys

class BTreeNode:
    def __init__(self, t, leaf=True):
        self.t = t; self.keys = []; self.children = []; self.leaf = leaf

class BTree:
    def __init__(self, t=3):
        self.t = t; self.root = BTreeNode(t)

    def search(self, key, node=None):
        node = node or self.root; i = 0
        while i < len(node.keys) and key > node.keys[i]: i += 1
        if i < len(node.keys) and key == node.keys[i]: return True
        if node.leaf: return False
        return self.search(key, node.children[i])

    def insert(self, key):
        r = self.root
        if len(r.keys) == 2 * self.t - 1:
            s = BTreeNode(self.t, False); s.children.append(self.root)
            self._split(s, 0); self.root = s
        self._insert_nonfull(self.root, key)

    def _insert_nonfull(self, node, key):
        i = len(node.keys) - 1
        if node.leaf:
            node.keys.append(0)
            while i >= 0 and key < node.keys[i]: node.keys[i+1] = node.keys[i]; i -= 1
            node.keys[i+1] = key
        else:
            while i >= 0 and key < node.keys[i]: i -= 1
            i += 1
            if len(node.children[i].keys) == 2 * self.t - 1:
                self._split(node, i)
                if key > node.keys[i]: i += 1
            self._insert_nonfull(node.children[i], key)

    def _split(self, parent, i):
        t = self.t; child = parent.children[i]
        new = BTreeNode(t, child.leaf)
        parent.keys.insert(i, child.keys[t-1])
        parent.children.insert(i+1, new)
        new.keys = child.keys[t:]; child.keys = child.keys[:t-1]
        if not child.leaf: new.children = child.children[t:]; child.children = child.children[:t]

    def display(self, node=None, level=0):
        node = node or self.root
        print("  " * level + f"[{', '.join(map(str, node.keys))}]")
        for child in node.children: self.display(child, level + 1)

    def inorder(self, node=None):
        node = node or self.root; result = []
        for i, key in enumerate(node.keys):
            if not node.leaf: result.extend(self.inorder(node.children[i]))
            result.append(key)
        if not node.leaf and node.children: result.extend(self.inorder(node.children[-1]))
        return result

def main():
    import random; random.seed(42)
    bt = BTree(t=3)
    vals = random.sample(range(100), 20)
    print(f"Inserting: {vals}")
    for v in vals: bt.insert(v)
    print("
B-Tree structure:"); bt.display()
    print(f"
Inorder: {bt.inorder()}")
    print(f"Search 50: {bt.search(50)}, Search {vals[0]}: {bt.search(vals[0])}")

if __name__ == "__main__": main()
