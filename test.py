from kdtree import KDTree
pts = [(2,3),(5,4),(9,6),(4,7),(8,1),(7,2)]
tree = KDTree(pts)
nearest, dist = tree.nearest((5,5))
assert nearest == (5,4)
results = tree.range_search((5,5), 3)
assert (5,4) in results
knn = tree.knn((5,5), 3)
assert len(knn) == 3
assert knn[0] == (5,4)
# Edge: single point
t2 = KDTree([(0,0)])
assert t2.nearest((1,1))[0] == (0,0)
print("kdtree tests passed")
