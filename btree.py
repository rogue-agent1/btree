#!/usr/bin/env python3
"""B-tree data structure with insert, search, and traversal."""
import sys
class BTree:
    class Node:
        def __init__(self,leaf=True): self.keys=[]; self.children=[]; self.leaf=leaf
    def __init__(self,t=3): self.root=self.Node(); self.t=t
    def search(self,k,node=None):
        node=node or self.root; i=0
        while i<len(node.keys) and k>node.keys[i]: i+=1
        if i<len(node.keys) and k==node.keys[i]: return True
        if node.leaf: return False
        return self.search(k,node.children[i])
    def insert(self,k):
        r=self.root
        if len(r.keys)==2*self.t-1:
            s=self.Node(False); s.children=[r]; self.root=s
            self._split(s,0); self._insert_nonfull(s,k)
        else: self._insert_nonfull(r,k)
    def _split(self,parent,i):
        t=self.t; y=parent.children[i]; z=self.Node(y.leaf)
        parent.keys.insert(i,y.keys[t-1])
        parent.children.insert(i+1,z)
        z.keys=y.keys[t:]; y.keys=y.keys[:t-1]
        if not y.leaf: z.children=y.children[t:]; y.children=y.children[:t]
    def _insert_nonfull(self,node,k):
        i=len(node.keys)-1
        if node.leaf:
            node.keys.append(0); 
            while i>=0 and k<node.keys[i]: node.keys[i+1]=node.keys[i]; i-=1
            node.keys[i+1]=k
        else:
            while i>=0 and k<node.keys[i]: i-=1
            i+=1
            if len(node.children[i].keys)==2*self.t-1:
                self._split(node,i)
                if k>node.keys[i]: i+=1
            self._insert_nonfull(node.children[i],k)
    def traverse(self,node=None):
        node=node or self.root; result=[]
        for i in range(len(node.keys)):
            if not node.leaf: result+=self.traverse(node.children[i])
            result.append(node.keys[i])
        if not node.leaf: result+=self.traverse(node.children[-1])
        return result
bt=BTree(3)
for x in [10,20,5,6,12,30,7,17,3,1,15,25,35,40,2]:
    bt.insert(x)
print(f"Sorted: {bt.traverse()}")
for k in [6,15,42]: print(f"Search {k}: {bt.search(k)}")
