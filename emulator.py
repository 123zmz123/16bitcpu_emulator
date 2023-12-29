from memory import Memory
from cpu import CPU
from instr import Instruction
ip=0;acc=1;r1=2;r2=3;r3=4;r4=5;r5=6;r6=7;r7=8;r8=9
ram = Memory(256*256)
i = 0
ram.raw_mem[i] = Instruction.MOV_MEM_REG
i+=1
ram.raw_mem[i]=0x01
i+=1
ram.raw_mem[i]=0x00
i+=1
ram.raw_mem[i]=r1
i+=1

ram.raw_mem[i]=Instruction.ADD_REG_REG
i+=1
ram.raw_mem[i]=r1
i+=1
ram.raw_mem[i]=r2
i+=1

ram.raw_mem[i]=Instruction.MOV_REG_MEM
i+=1
ram.raw_mem[i]=acc
i+=1
ram.raw_mem[i]=0x01
i+=1
ram.raw_mem[i]=0x02
i+=1

ram.raw_mem[i]=Instruction.JMP_NOT_EQ
i+=1
ram.raw_mem[i]=0x00
i+=1
ram.raw_mem[i]=0x03
i+=1
ram.raw_mem[i]=0x00
i+=1
ram.raw_mem[i]=0x00
i+=1

ram.raw_mem[0x0100] = 0xAA
ram.raw_mem[0x0101] = 0xBB

if __name__ == '__main__':
    _16bit = CPU(ram)
    _16bit.step()
    _16bit.step()
    _16bit.step()
    _16bit.step()
    _16bit.debug()
    _16bit.viewMemoryAt(0x0100)
    # _16bit.step()
    # _16bit.debug()
    # _16bit.step()
    # _16bit.debug()