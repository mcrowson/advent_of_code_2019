from aocd import data
from itertools import product
import copy

def get_output(noun, verb, dn):
    dn[1] = noun
    dn[2] = verb
    iterange = iter(range(len(dn)))

    for i in iterange:
        if dn[i] == 99:
            return dn[0]
        
        if dn[i] == 1:
            dn[dn[i+3]] = dn[dn[i+1]] + dn[dn[i+2]]
        elif dn[i] == 2:
            dn[dn[i+3]] = dn[dn[i+1]] * dn[dn[i+2]]

        [next(iterange) for i in range(3)]

datan = [int(d) for d in data.split(',')]
dn = copy.copy(datan)
p1 = get_output(12, 2, dn)
print(f"Part 1: {p1}")

for noun, verb in product(range(100), repeat=2):
    dn = copy.copy(datan)
    p2_candidate = get_output(noun, verb, dn)
    if p2_candidate == 19690720:
        p2hash = 100 * noun + verb
        print(f"Part 2: {p2hash}")
