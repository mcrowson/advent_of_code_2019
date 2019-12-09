from aocd import get_data
from itertools import permutations, cycle, chain
import copy
data = get_data(day=7)

'''  IGNORE THIS, old Part 1 stuff
def get_thruster_out(dn, seq, inp=0):
    s = seq.pop(0)
    o = get_output([s, inp], dn)
    if seq:
        return get_thruster_out(dn, seq, o)
    return o

#dn = [int(d) for d in data.split(',')]
#dn = copy.copy(datan)
#p1 = max([get_thruster_out(dn, list(prm)) for prm in permutations(range(5))])
'''

class Amp(object):
    def __init__(self, dn, phase):
        self.dn = dn  # memory
        self.i = 0  # Position in memory
        self.return_code = None # returned code  
        self.phase_input = [phase]  # holds input values
        self.state = 'pause' # Indicates paused when 4 or off when 99

    def _o(self, off, p): # Gets value at index+offset positional or immediate
        return self.dn[self.dn[self.i+off]] if p else self.dn[self.i+off]

    def run_machine(self, inp):
        self.phase_input.append(inp)  # Add new input to input lists

        while True:
            p = str(self.dn[self.i]).zfill(5)  # 1 -> 00001
            inst = p[3:]  # Instruction
            p2, p1 = p[1] == '0', p[2] == '0'  # positinoal/immediate for args 1 / 2 
            if inst == '99':  # end
                self.state = 'off'
                return
            elif inst == '01':  # add
                self.dn[self.dn[self.i+3]] = self._o(1, p1) + self._o(2, p2)
                self.i += 4
            elif inst == '02':  # multiply
                self.dn[self.dn[self.i+3]] = self._o(1, p1) * self._o(2, p2)
                self.i += 4
            elif inst == '03':  # store input
                self.dn[self.dn[self.i+1]] = self.phase_input.pop(0)
                self.i += 2
            elif inst == '04':  # give output
                self.return_code = self._o(1, p1)
                self.i += 2
                self.state = 'pause'
                return
            elif inst == '05':  # jump-if-true
                self.i = self._o(2, p2) if self._o(1, p1) != 0 else self.i + 3
            elif inst == '06':  # jump-if-false
                self.i = self._o(2, p2) if self._o(1, p1) == 0 else self.i + 3
            elif inst == '07':  # less than
                self.dn[self.dn[self.i+3]] = 1 if self._o(1, p1) < self._o(2, p2) else 0
                self.i += 4
            elif inst == '08':
                self.dn[self.dn[self.i+3]] = 1 if self._o(1, p1) == self._o(2, p2) else 0
                self.i += 4
            else:
                raise Exception("Got invalid instruction")
    

dn = [3,26,1001,26,-4,26,3,27,1002,27,2,27,1,27,26,27,4,27,1001,28,-1,28,1005,28,6,99,0,0,5] # 139629729
a, b, c, d, e = [Amp(dn, i) for i in [9,8,7,6,5]] # make amplifiers


while e.state != 'off':
    a.run_machine(e.return_code or 0)
    b.run_machine(a.return_code)
    c.run_machine(b.return_code)
    d.run_machine(c.return_code)
    e.run_machine(d.return_code)


print(e.return_code)

