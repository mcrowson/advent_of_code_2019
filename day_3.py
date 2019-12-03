from aocd import data

def get_coords(l_d):
    # Return coordinates from directions
    x, y = 0, 0
    l_points = set()
    for l in l_d:
        r = range(1, l['dist'] + 1)
        if l['dir'] == 'U':
            [l_points.add((x, y + i)) for i in r]
            y += l['dist']
        elif l['dir'] == 'D':
            [l_points.add((x, y - i)) for i in r]
            y -= l['dist']
        elif l['dir'] == 'R':
            [l_points.add((x + i, y)) for i in r]
            x += l['dist']
        else:
            [l_points.add((x - i, y)) for i in r]
            x -= l['dist']
    
    return l_points


#l1, l2 = data.split('\n')

# 159
l1 = 'R75,D30,R83,U83,L12,D49,R71,U7,L72'
l2 = 'U62,R66,U55,R34,D71,R55,D58,R83'

# 6
#l1 = 'R8,U5,L5,D3'
#l2 = 'U7,R6,D4,L4'

# 135
#l1 = 'R98,U47,R26,D63,R33,U87,L62,D20,R33,U53,R51'
#l2 = 'U98,R91,D20,R16,D67,R40,U7,R15,U6,R7'

l1_d = [{'dir': l[0], 'dist': int(l[1:])} for l in l1.split(',')]
l2_d = [{'dir': l[0], 'dist': int(l[1:])} for l in l2.split(',')]

l1_points = get_coords(l1_d)
l2_points = get_coords(l2_d)

intersections = l1_points.intersection(l2_points)
min_dist = min([l[0] + l[1] for l in intersections]) 
print(f'Part 1 {min_dist}')

