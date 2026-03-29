#!/usr/bin/env python3
"""K-D tree for spatial queries. Zero dependencies."""
import math

class KDNode:
    def __init__(self, point, left=None, right=None, axis=0):
        self.point = point; self.left = left; self.right = right; self.axis = axis

class KDTree:
    def __init__(self, points, k=2):
        self.k = k
        self.root = self._build(list(points), 0)

    def _build(self, points, depth):
        if not points: return None
        axis = depth % self.k
        points.sort(key=lambda p: p[axis])
        mid = len(points) // 2
        return KDNode(
            points[mid],
            self._build(points[:mid], depth+1),
            self._build(points[mid+1:], depth+1),
            axis
        )

    def nearest(self, target):
        best = [None, float("inf")]
        def _search(node):
            if not node: return
            d = math.hypot(*(target[i]-node.point[i] for i in range(self.k)))
            if d < best[1]: best[0] = node.point; best[1] = d
            diff = target[node.axis] - node.point[node.axis]
            close = node.left if diff < 0 else node.right
            far = node.right if diff < 0 else node.left
            _search(close)
            if abs(diff) < best[1]: _search(far)
        _search(self.root)
        return best[0], best[1]

    def range_search(self, center, radius):
        results = []
        def _search(node):
            if not node: return
            d = math.hypot(*(center[i]-node.point[i] for i in range(self.k)))
            if d <= radius: results.append(node.point)
            diff = center[node.axis] - node.point[node.axis]
            if diff - radius <= 0: _search(node.left)
            if diff + radius >= 0: _search(node.right)
        _search(self.root)
        return results

    def knn(self, target, k):
        import heapq
        heap = []
        def _search(node):
            if not node: return
            d = math.hypot(*(target[i]-node.point[i] for i in range(self.k)))
            if len(heap) < k: heapq.heappush(heap, (-d, node.point))
            elif d < -heap[0][0]: heapq.heapreplace(heap, (-d, node.point))
            diff = target[node.axis] - node.point[node.axis]
            close = node.left if diff < 0 else node.right
            far = node.right if diff < 0 else node.left
            _search(close)
            if len(heap) < k or abs(diff) < -heap[0][0]: _search(far)
        _search(self.root)
        return [p for _, p in sorted(heap, key=lambda x: -x[0])]

if __name__ == "__main__":
    tree = KDTree([(2,3),(5,4),(9,6),(4,7),(8,1),(7,2)])
    print(f"Nearest to (5,5): {tree.nearest((5,5))}")
