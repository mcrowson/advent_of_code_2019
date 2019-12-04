
p1_counter = 0
p2_counter = 0
for n in range(402328, 864247):
    ns = str(n)
    repeats = [ns.count(d) for d in set(ns)]

    if ns != ''.join(sorted(ns)) or max(repeats) < 2::
        continue  # Not increasing
    p1_counter += 1
    
    if 2 not in repeats:
        continue

    p2_counter += 1

print(f"Part 1: {p1_counter}")
print(f"Part 2: {p2_counter}")
