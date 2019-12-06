from aocd import data
from anytree import Node, RenderTree

datan = {(d[:3], d[4:]) for d in data.split('\n')}
data = 'B)C,C)D,D)E,E)F,B)G,G)H,D)I,E)J,J)K,K)L'
datan = {(d[:1], d[2:]) for d in data.split(',')}
datan.add(('COM', 'B'))
print('hi')
tree = {}
for p, c in datan:
    if p not in tree:
        tree[p] = Node(p)
    tree[c] = Node(c, parent=tree[p])

def parents(node, c=0):
    if not node.parent:
        return c
    p = tree[node.parent.name]
    c += 1
    return parents(p, c)

total = 0
for node in tree.values():
    total += node.depth


print(total)
