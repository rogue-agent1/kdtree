#!/usr/bin/env python3
"""KD-tree for nearest neighbor. Input: 'x y' per line, query as args."""
import sys, math
class Node:
    def __init__(self, pt, l=None, r=None, ax=0): self.pt,self.l,self.r,self.ax=pt,l,r,ax
def build(pts, d=0):
    if not pts: return None
    pts.sort(key=lambda p:p[d%len(p)]); m=len(pts)//2
    return Node(pts[m], build(pts[:m],d+1), build(pts[m+1:],d+1), d%len(pts[0]))
def nearest(node, target, best=None, best_d=float('inf')):
    if not node: return best, best_d
    d = math.dist(node.pt, target)
    if d < best_d: best, best_d = node.pt, d
    ax = node.ax; diff = target[ax]-node.pt[ax]
    close, far = (node.l, node.r) if diff<0 else (node.r, node.l)
    best, best_d = nearest(close, target, best, best_d)
    if abs(diff) < best_d: best, best_d = nearest(far, target, best, best_d)
    return best, best_d
pts = []
for line in sys.stdin:
    p = line.split()
    if len(p)>=2: pts.append(tuple(float(x) for x in p))
tree = build(pts)
q = tuple(float(x) for x in sys.argv[1:]) if len(sys.argv)>1 else pts[0]
nn, d = nearest(tree, q)
print(f"Query: {q}\nNearest: {nn}\nDistance: {d:.4f}")
