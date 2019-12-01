from bit_way.utils import *

def ldr(mem, reg, instruction):
    dst = barray_to_int(instruction[9:12])
    base = barray_to_int(instruction[6:9])
    offset = barray_to_int(instruction[0:6])
    address_to_load = barray_to_int(reg[base]) + offset
    print(barray_to_int(reg[base]), offset)
    reg[dst] = mem[address_to_load]


def ld(mem, reg, origin, destination):
    if origin.startswith('@'):
        reg[destination] = mem[int(origin[1:])]
    else:
        reg[destination] = origin


def sv(mem, reg, origin, destination):
    mem[destination] = reg[origin]