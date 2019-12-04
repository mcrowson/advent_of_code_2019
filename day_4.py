
p1_counter, p2_counter = 0, 0
for n in range(402328, 864247):
    ns = str(n)
    repeats = [ns.count(d) for d in set(ns)]
    if ns == ''.join(sorted(ns)) and max(repeats) >= 2:
        p1_counter += 1
        if 2 in repeats:
            p2_counter += 1 # part 2 needs a double

print(f"Part 1: {p1_counter}. Part 2: {p2_counter}")
