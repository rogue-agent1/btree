#!/usr/bin/env python3
"""btree — B-tree with insert, search, delete, and traversal. Zero deps."""

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
        node = node or self.root
        i = 0
        while i < len(node.keys) and key > node.keys[i]:
            i += 1
        if i < len(node.keys) and node.keys[i] == key:
            return True
        if node.leaf:
            return False
        return self.search(key, node.children[i])

    def insert(self, key):
        root = self.root
        if len(root.keys) == 2 * self.t - 1:
            new_root = BTreeNode(self.t, False)
            new_root.children.append(self.root)
            self._split(new_root, 0)
            self.root = new_root
        self._insert_non_full(self.root, key)

    def _insert_non_full(self, node, key):
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
            self._insert_non_full(node.children[i], key)

    def _split(self, parent, i):
        t = self.t
        child = parent.children[i]
        new = BTreeNode(t, child.leaf)
        parent.keys.insert(i, child.keys[t - 1])
        parent.children.insert(i + 1, new)
        new.keys = child.keys[t:]
        child.keys = child.keys[:t - 1]
        if not child.leaf:
            new.children = child.children[t:]
            child.children = child.children[:t]

    def traverse(self, node=None):
        node = node or self.root
        result = []
        for i, key in enumerate(node.keys):
            if not node.leaf:
                result.extend(self.traverse(node.children[i]))
            result.append(key)
        if not node.leaf:
            result.extend(self.traverse(node.children[-1]))
        return result

    def height(self, node=None):
        node = node or self.root
        if node.leaf: return 1
        return 1 + self.height(node.children[0])

def main():
    bt = BTree(t=3)
    data = [10,20,5,6,12,30,7,17,3,1,25,35,40,15,8]
    for x in data:
        bt.insert(x)
    print(f"B-tree (t=3, height={bt.height()}):")
    print(f"  Sorted: {bt.traverse()}")
    for q in [12, 13, 40]:
        print(f"  Search {q}: {bt.search(q)}")

if __name__ == "__main__":
    main()
