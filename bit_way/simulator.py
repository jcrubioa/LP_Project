import logging
import socket

logging.basicConfig()
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

HOST = '0.0.0.0'
PORT = 65656

class VNMachine:
    def __init__(self, mem_size, reg_size):
        self.mem_size = mem_size
        self.reg_size = reg_size
        self.pc = 0x10
        self.ri = ('', [])
        self.mem = [0 for i in range(mem_size)]
        self.reg = [0 for j in range(reg_size)]
        self.network = {}

    def load_code(self, code):
        instructions = iter(code.split('\n'))
        for i in range(0x10, 0xFF):
            while True:
                instruction = next(instructions, None)
                if instruction != '':
                    break
            if instruction is not None:
                self.mem[i] = int(instruction, 16)


    def execute(self):
        logger.info("EXECUTION")
        while True:
            logger.info("PC: {}".format(self.pc))
            logger.info("REG:")
            self.print_reg()
            logger.info("MEM:")
            self.print_mem()
            instruction = self.mem[self.pc]
            self.pc += 1

            op = (instruction >> 12) & 15  # bits 12-15
            d = (instruction >> 8) & 15  # bits 08-11
            s = (instruction >> 4) & 15  # bits 04-07
            t = (instruction >> 0) & 15  # bits 00-03
            addr = (instruction >> 0) & 255  # bits 00-07

            if op == 0:
                logger.debug('HALT')
                break
            elif op == 1:
                logger.debug('R[{d}] <- R[{s}] + R[{t}]'.format(
                    d=d, s=s, t=t
                ))
                self.reg[d] = self.reg[s] + self.reg[t]
            elif op == 2:
                logger.debug('R[{d}] <- R[{s}] - R[{t}]'.format(
                    d=d, s=s, t=t
                ))
                self.reg[d] = self.reg[s] - self.reg[t]
            elif op == 3:
                logger.debug('R[{d}] <- R[{s}] & R[{t}]'.format(
                    d=d, s=s, t=t
                ))
                self.reg[d] = self.reg[s] & self.reg[t]
            elif op == 4:
                logger.debug('R[{d}] <- R[{s}] ^ R[{t}]'.format(
                    d=d, s=s, t=t
                ))
                self.reg[d] = self.reg[s] ^ self.reg[t]
            elif op == 5:
                logger.debug('R[{d}] <- R[{s}] << R[{t}]'.format(
                    d=d, s=s, t=t
                ))
                self.reg[d] = self.reg[s] << self.reg[t]
            elif op == 6:
                logger.debug('R[{d}] <- R[{s}] >> R[{t}]'.format(
                    d=d, s=s, t=t
                ))
                self.reg[d] = self.reg[s] >> self.reg[t]
            elif op == 7:
                logger.debug('R[{d}] <- {addr}'.format(
                    d=d, addr=addr
                ))
                self.reg[d] = addr
            elif op == 8:
                logger.debug('R[{d}] <- mem[{addr}]'.format(
                    d=d, addr=addr
                ))
                self.reg[d] = self.mem[addr]
            elif op == 9:
                logger.debug('mem[{addr}] <- R[{d}]'.format(
                    addr=addr, d=d
                ))
                self.mem[addr] = self.reg[d]
            elif op == 10:
                logger.debug('R[{d}] <- mem[R[{t}]]'.format(
                    d=d, t=t
                ))
                self.reg[d] = self.mem[self.reg[t]]
            elif op == 11:
                logger.debug('mem[R[{t}]] <- R[{d}]'.format(
                    d=d, t=t
                ))
                self.mem[self.reg[t]] = self.reg[d]
            elif op == 12:
                logger.debug('IF R[{d}] == 0: pc = {addr}'.format(
                    d=d, addr=addr
                ))
                if self.reg[d] == 0:
                    self.pc = addr
            elif op == 13:
                logger.debug('IF R[{d}] > 0: pc = {addr}'.format(
                    d=d, addr=addr
                ))
                if self.reg[d] > 0:
                    self.pc = addr
            elif op == 14:
                logger.debug('pc = R[{d}]'.format(
                    d=d
                ))
                self.pc = self.reg[d]
            elif op == 15:
                logger.debug('R[{d}] = pc'.format(
                    d=d
                ))
                self.reg[d] = self.pc
                self.pc = addr
    def print_mem(self):
        to_print = ''
        for i, e in enumerate(self.mem):
            if e != 0:
                to_print += " | {}: {}".format(i, e)
        logger.info(to_print + "|")

    def print_reg(self):
        to_print = ''
        for i, e in enumerate(self.reg):
            if e != 0:
                to_print += " | {}: {}".format(i, e)
        logger.info(to_print + "|")

    def init_socket_server(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind((HOST, PORT))
            s.listen()


input_code = """
8C00
8AFF
CA15
1CCA
C011
9CFF
0000
"""

vn = VNMachine(256, 16)
vn.mem[255] = 1
vn.load_code(input_code)
vn.execute()

