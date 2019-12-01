from bit_way.vm_instructions_1 import *

from bit_way.utils import *

class VNMachine:
    def __init__(self, mem_size, reg_size, instruction_set):
        self.mem_size = mem_size
        self.reg_size = reg_size
        self.cp = 0
        self.ri = ('', [])
        self.instruction_set = instruction_set
        self.mem = [[False for i in range(16)] for i in range(mem_size)]
        self.reg = [[False for i in range(16)] for j in range(reg_size)]

    def compile(self, code):
        c = 0
        for line in code.split("\n"):
            line = line.strip(' ')
            if line == '':
                continue
            instruction, comment = line.split(';')
            instruction = instruction.strip(' ')
            if instruction == '':
                continue
            print("LINE: {}".format(line))
            self.mem[c] = instruction.split(' ')

            print("MEM: {}".format(self.get_mem()))
            print("REG: {}".format(self.get_reg()))
            c += 1

    def execute(self):
        print("EXECUTION")
        while self.cp < self.mem_size:
            print("CP: {}".format(self.cp))
            print("MEM: {}".format(self.mem[self.cp]))
            print("REG: {}".format(self.get_reg()))
            instruction = self.mem[self.cp]
            command, *args = instruction
            if command == 'end':
                break
            INSTRUCTIONS[command](self.mem, self.reg, instruction)
            self.cp += 1
            # ri = command, params
            # INSTRUCTIONS[command](self.mem, self.reg, *params)
            # cp += 1

    def get_mem(self):
        return [barray_to_int(x) for x in self.mem]

    def get_reg(self):
        return [barray_to_int(x) for x in self.reg]


END = 0
LDR = 1
LD = 2
SV = 3

INSTRUCTIONS = {
    'ldr': ldr,
    'ld': ld,
    'sv': sv,
    'end': END
}

input_code = """
ld 5 3;
ld 0 1;
sv 6 5;
ldr 2 0 1;
"""

vn = VNMachine(16, 10, INSTRUCTIONS)
vn.compile(input_code)
vn.execute()

print(vn.get_reg())
print(vn.get_mem())
