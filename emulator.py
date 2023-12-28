from memory import Memory
from cpu import CPU
from instr import Instruction
ram = Memory(1024)
ram.raw_mem[0] = Instruction.MOVE_LIT_R1
ram.raw_mem[1] = 0x12
ram.raw_mem[2] = 0x34

ram.raw_mem[3] = Instruction.MOVE_LIT_R2
ram.raw_mem[4] = 0xAB
ram.raw_mem[5] = 0xCD

ram.raw_mem[6] = Instruction.ADD_REG_REG
ram.raw_mem[7] = 0x01
ram.raw_mem[8] = 0x02
if __name__ == '__main__':
    _16bit = CPU(ram)
    _16bit.debug()
    _16bit.step()
    _16bit.debug()
    _16bit.step()
    _16bit.debug()
    _16bit.step()
    _16bit.debug()