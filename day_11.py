import matplotlib.pyplot as plt
import numpy as np
from aocd import get_data, submit
from itertools import cycle
import copy


data = [int(d) for d in get_data(day=11).split(',')]

class IntCode(object):
    def __init__(self, dn, phase=None):
        self.dn = copy.copy(dn)  # memory
        self.i = 0  # Position in memory
        self.rel_base = 0  # relative base
        self.return_codes = [] # returned codes
        self.phase_input = [phase] if phase else []  # holds input values
        self.state = 'on' # turns off at 99
        self.buffer = []  # two values we return each time

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
        self.buffer = []  # reset buffer
        if inp:
            self.phase_input.append(inp)  # Add new input to input lists

        while True:
            p = str(self._get(self.i)).zfill(5)  # 1 -> 00001
            inst = p[3:]  # Instruction
            p3, p2, p1 = p[0], p[1], p[2]  # positinoal/immediate for args 1 / 2 
            if inst == '99':  # end
                self.state = 'off'
                return None, 0
            elif inst == '01':  # add
                self._save(self._get_pos(3, p3), self._get_val(1, p1) + self._get_val(2, p2))
                self.i += 4
            elif inst == '02':  # multiply
                self._save(self._get_pos(3, p3), self._get_val(1, p1) * self._get_val(2, p2))
                self.i += 4
            elif inst == '03':  # store input
                self._save(self._get_pos(1, p1), self.phase_input.pop(0))
                self.i += 2
            elif inst == '04':  # give output
                self.return_codes.append(self._get_val(1, p1))
                self.buffer.append(self._get_val(1, p1))
                self.i += 2
                if len(self.buffer) == 2:
                    return self.buffer
                
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

seen = {}
pos = (0, 0)
comp = IntCode(dn=data)
dirs = [0, 1, 2, 3]  # up, right, down, left
facing = dirs[0]

while comp.state == 'on':
    current = seen[pos] if pos in seen else '0' 
    color, d = comp.run_machine(inp=current)
    if color is None:
        break  # 99
    seen[pos] = color
    if d == 0:  # turn left
        facing = dirs[(facing + 3)%4]
    elif d ==1 :  # turn right
        facing = dirs[(facing + 1)%4]
    else:
        raise Exception("Invalid direction")

    if facing == 0:  # up
        pos = (pos[0], pos[1] + 1)
    elif facing == 1:  # right
        pos = (pos[0] + 1, pos[1])
    elif facing == 2: # down
        pos = (pos[0], pos[1] - 1)
    elif facing == 3:  # 'left'
        pos = (pos[0] - 1, pos[1])
    else:
        raise Exception("Invalid position")


print(f'Part 1: {len(seen)}')


# Save to img 
xmin = min([k[0] for k in seen.keys()])
ymin = min([k[1] for k in seen.keys()])

x = max([k[0] for k in seen.keys()]) - xmin
y = max([k[1] for k in seen.keys()]) - ymin
canvas = np.full((x+1, y+1), 2)

for k, v in seen.items():
    canvas[k[0] + abs(xmin)][k[1] + abs(ymin)] = v

plt.imshow(np.array(canvas))
plt.savefig('day_11.png')

# validate same as len(seen)
not_2 = sum([len([v for v in r if v != 2]) for r in canvas])
print(not_2)