from aocd import get_data
from collections import defaultdict
from itertools import product
from math import sqrt, pow

data = get_data(day=10)
dn = data.split('\n')

combos = list(product(range(len(dn[0])), range(len(dn))))


ast_points = [p for p in combos if dn[p[1]][p[0]] == '#']
ast_slopes = defaultdict(lambda: defaultdict(list))
'''
dict contains each point. For each point we have another dict whose keys are 
slopes found for that relationship and the keys present.

R is used for points in quadrants 1/2 and L for 3/4

ast_slopes = {
    (0,0): {
        'R-1': [(0, 2), (0,4)]
        'R-1.2': [(1, 2), (5,4)]
    }
}
'''
for ast in ast_points:
    for other in ast_points:
        if ast == other:
            continue
        xd = other[0] - ast[0]
        yd = ast[1] - other[1]
        if xd == 0: # up/down
            if ast[1] > other[1]:
                ast_slopes[ast]['up'].append(other)
            else:
                ast_slopes[ast]['down'].append(other)
        elif yd == 0: #left/right
            if ast[0] > other[0]:
                ast_slopes[ast]['left'].append(other)
            else:
                ast_slopes[ast]['right'].append(other)
        else:
            sl = yd/xd
            d = 'L' if other[0] < ast[0] else 'R'
            ast_slopes[ast][f"{d}{sl}"].append(other)

most_visible = max(ast_slopes, key=lambda v: len(ast_slopes[v]))
mv = ast_slopes[most_visible]
print(f"P1: {most_visible} can see {len(mv)}")

def dist(p1, p2=most_visible):
    return sqrt(pow(p1[0] - p2[0], 2) + pow(p1[1] - p2[1], 2))

# order each of the slopes by ascending distance
for sl, others in mv.items():
    mv[sl] = sorted(others, key=dist)
    if (12, 1) in others:
        this = '1'

# Put slopes into their quardants and order them the direction the gun spins
q1_slopes = sorted([float(s[1:]) for s in mv.keys() if s[0] == 'R' and s[1] != '-'], reverse=True)
q2_slopes = sorted([float(s[1:]) for s in mv.keys() if s[0] == 'R' and s[1] == '-'], reverse=True)
q3_slopes = sorted([float(s[1:]) for s in mv.keys() if s[0] == 'L' and s[1] != '-'], reverse=True)
q4_slopes = sorted([float(s[1:]) for s in mv.keys() if s[0] == 'L' and s[1] == '-'], reverse=True)

shot = []
while len(shot) < 200:
    # up
    if mv['up']:
        d = mv['up'].pop(0)
        shot.append(d)
    # q1
    for sl in q1_slopes:
        if mv[f'R{sl}']:
            d = mv[f'R{sl}'].pop(0)
            shot.append(d)
    # right
    if mv['right']:
        d = mv['right'].pop(0)
        shot.append(d)
    # q2
    for sl in q2_slopes:
        if mv[f'R{sl}']:
            d = mv[f'R{sl}'].pop(0)
            shot.append(d)
    # down
    if mv['down']:
        d = mv['down'].pop(0)
        shot.append(d)
    # q3
    for sl in q3_slopes:
        if mv[f'L{sl}']:
            d = mv[f'L{sl}'].pop(0)
            shot.append(d)
    # left
    if mv['left']:
        d = mv['left'].pop(0)
        shot.append(d)
    # q4
    for sl in q4_slopes:
        if mv[f'L{sl}']:
            d = mv[f'L{sl}'].pop(0)
            shot.append(d)

th_shot = shot[199]
print(f"P2: {th_shot} is the 200th shot and its checksum is {th_shot[0] * 100 + th_shot[1]}")