from aocd import data
import copy

dn = [int(d) for d in data.split(',')]
dn[1] = 12
dn[2] = 2

dn_f = copy.copy(dn)

dn_rows = []

while dn:
    if dn[0] == 99:
        dn_rows.append([dn[0]])
        del dn[0]
    else:
        dn_rows.append(dn[0:4])
        del dn[0:4]

for o in dn_rows:
    if o[0] == 99:
        print("Part 1: {}".format(dn_rows[0][0]))
        break

    col = o[3] // 4
    row = o[3] % 4
    
    if o[0] == 1:
        r = dn_f[o[1]] + dn_f[o[2]]
        dn_rows[col][row] += r
    elif o[0] == 2:
        r = dn_f[o[1]] * dn_f[o[2]]
        dn_rows[col][row] *= r

    