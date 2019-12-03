from aocd import data

def get_coords(l_d):
    # Return coordinates from directions
    x, y = 0, 0
    cum_d = 0  # Track cumulative distance for each point on path
    l_points = []
    for l in l_d:
        r = range(1, l['dist'] + 1)  # Add each point along the path
        if l['dir'] == 'U':
            [l_points.append({'p':(x, y + i), 'd': cum_d+i}) for i in r]
            y += l['dist']
        elif l['dir'] == 'D':
            [l_points.append({'p':(x, y - i), 'd': cum_d+i}) for i in r]
            y -= l['dist']
        elif l['dir'] == 'R':
            [l_points.append({'p': (x + i, y), 'd': cum_d+i}) for i in r]
            x += l['dist']
        else:
            [l_points.append({'p': (x - i, y), 'd': cum_d+i}) for i in r]
            x -= l['dist']
        cum_d += l['dist']
    
    return l_points

# make lists of dicts with direction and distance
l1_d, l2_d = [[{'dir': l[0], 'dist': int(l[1:])} for l in ln.split(',')] for ln in data.split('\n')]

l1_points = get_coords(l1_d)
l2_points = get_coords(l2_d)
# list to set to find intersection of points
intersections = set([l['p'] for l in l1_points]).intersection(set([l['p'] for l in l2_points]))
min_dist = min([abs(l[0]) + abs(l[1]) for l in intersections]) 
print(f'Part 1: {min_dist}')

travel_times_to_int = []
for i in intersections:
    l1_first = min([l['d'] for l in l1_points if l['p'] == i]) # possibly crosses point multiple times, find lowest cum_d
    l2_first = min([l['d'] for l in l2_points if l['p'] == i])
    travel_times_to_int.append(l1_first + l2_first)

min_trav = min(travel_times_to_int)
print(f'Part 2: {min_trav}')