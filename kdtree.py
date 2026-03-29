#!/usr/bin/env python3
"""kdtree: K-D tree for spatial search."""
import math, sys

class KDNode:
    def __init__(self, point, left=None, right=None, axis=0):
        self.point = point; self.left = left; self.right = right; self.axis = axis

def build(points, depth=0):
    if not points: return None
    k = len(points[0])
    axis = depth % k
    points.sort(key=lambda p: p[axis])
    mid = len(points) // 2
    return KDNode(
        point=points[mid],
        left=build(points[:mid], depth+1),
        right=build(points[mid+1:], depth+1),
        axis=axis
    )

def nearest(root, target, best=None, best_dist=float('inf')):
    if root is None: return best, best_dist
    d = math.sqrt(sum((a-b)**2 for a,b in zip(root.point, target)))
    if d < best_dist:
        best, best_dist = root.point, d
    axis = root.axis
    diff = target[axis] - root.point[axis]
    close = root.left if diff <= 0 else root.right
    far = root.right if diff <= 0 else root.left
    best, best_dist = nearest(close, target, best, best_dist)
    if abs(diff) < best_dist:
        best, best_dist = nearest(far, target, best, best_dist)
    return best, best_dist

def range_search(root, lo, hi, results=None):
    if results is None: results = []
    if root is None: return results
    if all(lo[i] <= root.point[i] <= hi[i] for i in range(len(lo))):
        results.append(root.point)
    axis = root.axis
    if lo[axis] <= root.point[axis]:
        range_search(root.left, lo, hi, results)
    if hi[axis] >= root.point[axis]:
        range_search(root.right, lo, hi, results)
    return results

def test():
    pts = [(2,3),(5,4),(9,6),(4,7),(8,1),(7,2)]
    tree = build(list(pts))
    # Nearest
    point, dist = nearest(tree, (5,5))
    assert point == (5,4)
    assert abs(dist - 1.0) < 0.001
    # Exact match
    point2, dist2 = nearest(tree, (9,6))
    assert dist2 == 0
    # Range search
    results = range_search(tree, (3,2), (8,5))
    assert (5,4) in results
    assert (7,2) in results
    assert (9,6) not in results
    # Single point
    tree2 = build([(1,1)])
    p, d = nearest(tree2, (0,0))
    assert p == (1,1)
    print("All tests passed!")

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "test": test()
    else: print("Usage: kdtree.py test")
