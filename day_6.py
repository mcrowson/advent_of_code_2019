from aocd import data
from anytree import Node, Walker

datan = {(d[:3], d[4:]) for d in data.split('\n')}

tree = {p: Node(p) for p, c in datan} # Create tree with parent nodes
for p, c in datan: # Second pass to assign parent nodes 
    if c in tree:
        tree[c].parent = tree[p]
    else:
        tree[c] = Node(c, parent=tree[p])

total = sum([n.depth for n in tree.values()])
print(f"Part 1: {total}")

w = Walker()
path = w.walk(tree['YOU'].parent, tree['SAN'].parent)
dist = len(path[0]) + len(path[2])
print(f"Part 2: {dist}")