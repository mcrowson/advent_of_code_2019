from aocd import get_data
import copy


class Boost(object):
    def __init__(self, dn, phase=None):
        self.dn = copy.copy(dn)  # memory
        self.i = 0  # Position in memory
        self.rel_base = 0  # relative base
        self.return_codes = [] # returned codes
        self.phase_input = [phase] if phase else []  # holds input values

    def _expand(self, pos): # expand memory if needed
        self.dn = self.dn + [0 for _ in range(pos + 1 - len(self.dn))] if pos + 1 > len(self.dn) else self.dn

    def _get(self, pos): # return position, creates if does not exist
        self._expand(pos)
        return self.dn[pos]

    def _save(self, pos, val): # save to position, creates if does not exist
        self._expand(pos)
        self.dn[pos] = val

    def _o(self, off, p):
        if p == '0':  # Positional
            pos = self._get(self.i+off)
        elif p == '1':  # Imediate
            pos = self.i+off
        else: # p==2 Relative
            pos = self.rel_base+off
        
        return self._get(pos) 
        
    def run_machine(self, inp=None):
        if inp:
            self.phase_input.append(inp)  # Add new input to input lists

        while True:
            p = str(self._get(self.i)).zfill(5)  # 1 -> 00001
            inst = p[3:]  # Instruction
            p2, p1 = p[1] , p[2]  # positinoal/immediate for args 1 / 2 
            if inst == '99':  # end
                return self.return_codes[-1]
            elif inst == '01':  # add
                self._save(self._get(self.i+3), self._o(1, p1) + self._o(2, p2))
                self.i += 4
            elif inst == '02':  # multiply
                self._save(self._get(self.i+3), self._o(1, p1) * self._o(2, p2))
                self.i += 4
            elif inst == '03':  # store input
                self._save(self._get(self.i+1), self.phase_input.pop(0))
                self.i += 2
            elif inst == '04':  # give output
                self.return_codes.append(self._o(1, p1))
                print(self.return_codes[-1])
                self.i += 2
            elif inst == '05':  # jump-if-true
                self.i = self._o(2, p2) if self._o(1, p1) != 0 else self.i + 3
            elif inst == '06':  # jump-if-false
                self.i = self._o(2, p2) if self._o(1, p1) == 0 else self.i + 3
            elif inst == '07':  # less than
                self._save(self._get(self.i+3), 1 if self._o(1, p1) < self._o(2, p2) else 0)
                self.i += 4
            elif inst == '08':  # equality
                self._save(self._get(self.i+3), 1 if self._o(1, p1) == self._o(2, p2) else 0)
                self.i += 4
            elif inst == '09': # adjust relative parameter
                self.rel_base += self._o(1, p1)
                self.i += 2

            else:
                raise Exception("Got invalid instruction")


#data = get_data(day=9)
#dn = [int(n) for n in data.split(',')]

dn = [109,1,204,-1,1001,100,1,100,1008,100,16,101,1006,101,0,99]  # outputs self
b = Boost(dn)
b.run_machine(inp=None)