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
    def __init__(self, dn, phase):
        self.dn = dn
        self.return_codes = []
        self.inp_code_pos = 0  # position in source's return codes to look from
        self.phase_input = [phase]
        self.i = None  # Position in memory to resume from
        self.state = None # Indicates paused when yielded or off when terminated

    def _o(self, i, off, p): # Gets value at index+offset positional or immediate
        return self.dn[self.dn[i+off]] if p else self.dn[i+off]

    def run_machine(self, inp):
        # inp list of inputs
        # dn is instruction set
        if self.state == 'off':
            return

        i = self.i if self.i else 0
        inp = inp[self.inp_code_pos:]
        if not inp:
            return  #nothing new
        self.phase_input += inp
        self.inp_code_pos += len(inp)

        while True:
            p = str(self.dn[i]).zfill(4)
            inst = p[2:]
            p2, p1 = [v == '0' for v in p[:2]]
            if inst == '99':  # end
                self.state = 'off'
                return
            elif inst == '01':  # add
                self.dn[self.dn[i+3]] = self._o(i, 1, p1) + self._o(i, 2, p2)
                i += 4
            elif inst == '02':  # multiply
                self.dn[self.dn[i+3]] = self._o(i, 1, p1) * self._o(i, 2, p2)
                i += 4
            elif inst == '03':  # store input
                if self.phase_input:
                    self.dn[self.dn[i+1]] = self.phase_input.pop(0)
                    i += 2
                else:
                    self.i = i
                    self.state = 'pause'
                    return
            elif inst == '04':  # print value
                self.return_codes.append(self._o(i, 1, p1))
                i += 2
            elif inst == '05':  # jump-if-true
                ui = self._o(i, 1, p1)
                ij = self._o(i, 2, p2)
                i = self._o(i, 2, p2) if self._o(i, 1, p1) != 0 else i + 3
            elif inst == '06':  # jump-if-false
                i = self._o(i, 2, p2) if self._o(i, 1, p1) == 0 else i + 3
            elif inst == '07':  # less than
                self.dn[self.dn[i+3]] = 1 if self._o(i, 1, p1) < self._o(i, 2, p2) else 0
                i += 4
            elif inst == '08':
                self.dn[self.dn[i+3]] = 1 if self._o(i, 1, p1) == self._o(i, 2, p2) else 0
                i += 4
            else:
                raise Exception("Got invalid instruction")
    
a, b, c, d, e = [Amp(dn, i) for i in [9, 8, 7, 6, 5]] # make amplifiers
e.return_codes.append(0)

while e.state != 'off':
    a.run_machine(e.return_codes)
    b.run_machine(a.return_codes)
    c.run_machine(b.return_codes)
    d.run_machine(c.return_codes)
    e.run_machine(d.return_codes)


print(e.return_codes[-1])
#print(f"Part 1: {p1}")

