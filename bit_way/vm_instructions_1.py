from bit_way.utils import *

def ldr(mem, reg, instruction):
    dst = barray_to_int(instruction[9:12])
    base = barray_to_int(instruction[6:9])
    offset = barray_to_int(instruction[0:6])
    address_to_load = barray_to_int(reg[base]) + offset
    print(barray_to_int(reg[base]), offset)
    reg[dst] = mem[address_to_load]

def ld(mem, reg, instruction):
    dst = barray_to_int(instruction[9:12])
    value = barray_to_int(instruction[0:9])
    reg[dst] = int_to_barray(value, 16)

def sv(mem, reg, instruction):
    dst = barray_to_int(instruction[9:12])
    org = barray_to_int(instruction[6:9])
    mem[dst] = reg[org]
