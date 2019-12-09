from aocd import get_data
import matplotlib.pyplot as plt
import numpy as np

data = get_data(day=8)
dn = list(data)

w = 25
h = 6
layer_s = w * h

layers = [[dn[x:x+layer_s][y:y+w] for y in range(0, layer_s, w)] for x in range(0, len(dn), layer_s)]

zero_counts = [sum([r.count('0') for r in l]) for l in layers]
min_z_i = zero_counts.index(min(zero_counts))

p1 = sum([r.count('1') for r in layers[min_z_i]]) * sum([r.count('2') for r in layers[min_z_i]])
print(f"Part 1: {p1}")

canvas = np.full((h, w), 2)
for i in range(h):
    for j in range(w):
        for l in layers:
            if l[i][j] != '2':
                canvas[i][j] = int(l[i][j])
                break

plt.imshow(np.array(canvas))
plt.savefig('day_8.png')
print("See day_8.png for Part 2")