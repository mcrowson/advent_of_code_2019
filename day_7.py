from aocd import get_data
from itertools import permutations, cycle, chain
import copy
data = get_data(day=7)




def get_thruster_out(dn, seq, inp=0):
    s = seq.pop(0)
    o = get_output([s, inp], dn)
    if seq:
        return get_thruster_out(dn, seq, o)
    return o

#dn = [int(d) for d in data.split(',')]
#dn = copy.copy(datan)
#p1 = max([get_thruster_out(dn, list(prm)) for prm in permutations(range(5))])

dn = [3,26,1001,26,-4,26,3,27,1002,27,2,27,1,27,26,27,4,27,1001,28,-1,28,1005,28,6,99,0,0,5] # 139629729

class Amp(object):
    def __init__(self, dn):
        self.dn = dn
        self.return_code = None

    def _o(self, i, off, p): # Gets value at index+offset positional or immediate
        return self.dn[self.dn[i+off]] if p else self.dn[i+off]

    def get_output(self, inp):
        # inp list of inputs
        # dn is instruction set
        i = 0

        while True:
            p = str(self.dn[i]).zfill(4)
            inst = p[2:]
            p2, p1 = [v == '0' for v in p[:2]]
            if inst == '99':  # end
                return self.return_code
            elif inst == '01':  # add
                self.dn[self.dn[i+3]] = self._o(i, 1, p1) + self._o(i, 2, p2)
                i += 4
            elif inst == '02':  # multiple
                self.dn[self.dn[i+3]] = self._o(i, 1, p1) * self._o(i, 2, p2)
                i += 4
            elif inst == '03':  # store input
                self.dn[self.dn[i+1]] = inp.pop(0)
                i += 2
            elif inst == '04':  # print value
                self.return_code = self._o(i, 1, p1)
                i += 2
            elif inst == '05':  # jump-if-true
                i = self._o(i, 2, p2) if self._o(i, 1, p1) else i + 3
            elif inst == '06':  # jump-if-false
                i = self._o(i, 2, p2) if not self._o(i, 1, p1) else i + 3
            elif inst == '07':  # less than
                self.dn[self.dn[i+3]] = 1 if self._o(i, 1, p1) < self._o(i, 2, p2) else 0
                i += 4
            elif inst == '08':
                self.dn[self.dn[i+3]] = 1 if self._o(i, 1, p1) == self._o(i, 2, p2) else 0
                i += 4
            else:
                raise Exception("Got invalid instruction")
    
a, b, c, d, e = [Amp(copy.copy(dn)) for _ in range(5)] # make amplifiers

thrusts = []
for pass1 in permutations(range(5)):
    for pass2 in permutations(range(5, 10)):
        ao = a.get_output([0, pass1[0]])
        bo = b.get_output([ao, pass1[1]])
        co = c.get_output([bo, pass1[2]])
        do = d.get_output([co, pass1[3]])
        eo = e.get_output([do, pass1[4]])
        ao2 = a.get_output([eo, pass2[0]])
        bo2 = b.get_output([ao2, pass2[1]])
        co2 = c.get_output([bo2, pass2[2]])
        do2 = d.get_output([co2, pass2[3]])
        eo2 = e.get_output([do2, pass2[4]])
        thrusts.append(eo2)

print(max(thrusts))
#print(f"Part 1: {p1}")

