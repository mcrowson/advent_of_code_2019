from aocd import get_data
import copy
data = get_data(day=5)

def get_output(inp, dn):
    i = 0
    ret_code = None

    o1 = lambda: dn[dn[i+1]] if p1 else dn[i+1]
    o2 = lambda: dn[dn[i+2]] if p2 else dn[i+2]
    while True:
        p = str(dn[i]).zfill(4)
        inst = p[2:]
        p2, p1 = [v == '0' for v in p[:2]]
        if inst == '99':  # end
            return ret_code
        elif inst == '01':  # add
            dn[dn[i+3]] = o1() + o2()
            i += 4
        elif inst == '02':  # multiple
            dn[dn[i+3]] = o1() * o2()
            i += 4
        elif inst == '03':  # store input
            dn[dn[i+1]] = inp
            i += 2
        elif inst == '04':  # print value
            ret_code = o1()
            i += 2
        elif inst == '05':  # jump-if-true
            i = o2() if o1() else i + 3
        elif inst == '06':  # jump-if-false
            i = o2() if not o1() else i + 3
        elif inst == '07':  # less than
            dn[dn[i+3]] = 1 if o1() < o2() else 0
            i += 4
        elif inst == '08':
            dn[dn[i+3]] = 1 if o1() == o2() else 0
            i += 4
        
datan = [int(d) for d in data.split(',')]
dn = copy.copy(datan)
p1 = get_output(1, dn)
print(f"Part 1: {p1}")
dn = copy.copy(datan)
p2 = get_output(5, dn)
print(f"Part 2: {p2}")

