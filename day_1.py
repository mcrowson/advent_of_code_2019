from aocd import data
dn = [int(d) for d in data.split()]

r1 = sum(d//3-2 for d in dn)
print(r1)

def recurse_r2(mass):
    fuel_for_mass = mass//3-2
    if fuel_for_mass >= 1:
        return mass + recurse_r2(fuel_for_mass)
    return mass

r2 = sum(recurse_r2(d) for d in dn) - sum(dn)
print(r2)