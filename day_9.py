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

    def _get_pos(self, off, p):
        if p == '0':  # Positional
            pos = self._get(self.i+off)
        elif p == '1':  # Imediate
            pos = self.i+off
        else: # p==2 Relative
            pos = self.rel_base+ self._get(self.i + off)
        return pos

    def _get_val(self, off, p):
        return self._get(self._get_pos(off, p)) 
        
    def run_machine(self, inp=None):
        if inp:
            self.phase_input.append(inp)  # Add new input to input lists

        while True:
            p = str(self._get(self.i)).zfill(5)  # 1 -> 00001
            inst = p[3:]  # Instruction
            p3, p2, p1 = p[0], p[1], p[2]  # positinoal/immediate for args 1 / 2 
            if inst == '99':  # end
                return self.return_codes[-1]
            elif inst == '01':  # add
                self._save(self._get_pos(3, p3), self._get_val(1, p1) + self._get_val(2, p2))
                self.i += 4
            elif inst == '02':  # multiply
                self._save(self._get_pos(3, p3), self._get_val(1, p1) * self._get_val(2, p2))
                self.i += 4
            elif inst == '03':  # store input
                self._save(self._get_pos(1, p1), self.phase_input.pop(0))
                #print(self._get(self.rel_base))
                self.i += 2
            elif inst == '04':  # give output
                self.return_codes.append(self._get_val(1, p1))
                print(self.return_codes[-1])
                self.i += 2
            elif inst == '05':  # jump-if-true
                self.i = self._get_val(2, p2) if self._get_val(1, p1) != 0 else self.i + 3
            elif inst == '06':  # jump-if-false
                self.i = self._get_val(2, p2) if self._get_val(1, p1) == 0 else self.i + 3
            elif inst == '07':  # less than
                self._save(self._get_pos(3, p3), 1 if self._get_val(1, p1) < self._get_val(2, p2) else 0)
                self.i += 4
            elif inst == '08':  # equality
                self._save(self._get_pos(3, p3), 1 if self._get_val(1, p1) == self._get_val(2, p2) else 0)
                self.i += 4
            elif inst == '09': # adjust relative parameter
                self.rel_base += self._get_val(1, p1)
                self.i += 2

            else:
                raise Exception("Got invalid instruction")


data = get_data(day=9)
dn = [int(n) for n in data.split(',')]

b1 = Boost(dn)
p1 = b1.run_machine(inp=1)

b2 = Boost(dn)
p2 = p1 = b2.run_machine(inp=2)