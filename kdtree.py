#!/usr/bin/env python3
"""K-D tree for nearest neighbor search."""
import sys,math
class KDNode:
    def __init__(self,point,left=None,right=None,axis=0):
        self.point=point;self.left=left;self.right=right;self.axis=axis
def build(points,depth=0):
    if not points: return None
    k=len(points[0]); axis=depth%k
    points.sort(key=lambda p:p[axis])
    mid=len(points)//2
    return KDNode(points[mid],build(points[:mid],depth+1),build(points[mid+1:],depth+1),axis)
def dist(a,b): return math.sqrt(sum((x-y)**2 for x,y in zip(a,b)))
def nearest(root,target,best=None,best_dist=float('inf')):
    if root is None: return best,best_dist
    d=dist(root.point,target)
    if d<best_dist: best,best_dist=root.point,d
    axis=root.axis; diff=target[axis]-root.point[axis]
    close,far=(root.left,root.right) if diff<0 else (root.right,root.left)
    best,best_dist=nearest(close,target,best,best_dist)
    if abs(diff)<best_dist:
        best,best_dist=nearest(far,target,best,best_dist)
    return best,best_dist
def main():
    import random; random.seed(42)
    pts=[(random.uniform(0,100),random.uniform(0,100)) for _ in range(1000)]
    tree=build(list(pts))
    query=(50.0,50.0)
    nn,d=nearest(tree,query)
    brute=min(pts,key=lambda p:dist(p,query))
    print(f"Query: {query}")
    print(f"KD-tree nearest: {nn} (dist={d:.4f})")
    print(f"Brute force:     {brute} (dist={dist(brute,query):.4f})")
    print(f"Match: {'✓' if nn==brute else '✗'}")
if __name__=="__main__": main()
