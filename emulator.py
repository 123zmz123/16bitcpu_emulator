from memory import Memory
from memorymapper import MemoryMapper
from screen_device import Screen
from cpu import CPU
from instr import Instruction
ip=0;acc=1;r1=2;r2=3;r3=4;r4=5;r5=6;r6=7;r7=8;r8=9;sp=10;fp=11
ram = Memory(256*256)
subroutineAddress = 0x3000
waitSubroutineAddress = 0x3100
i = 0

def writeCharToScreen(char,command,position):
    global i
    ram.raw_mem[i] = Instruction.MOV_LIT_REG;i+=1
    ram.raw_mem[i] = command; i+=1
    ram.raw_mem[i] = (ord(char) & 0xFF); i+=1
    ram.raw_mem[i] = r1 ; i+=1

    ram.raw_mem[i] = Instruction.MOV_REG_MEM;i+=1
    ram.raw_mem[i] = r1; i+=1
    ram.raw_mem[i] = 0x30; i+=1
    ram.raw_mem[i] = position; i+=1

def process():
    ram_unit = MemoryMapper()
    screen_dev = Screen()
    writeCharToScreen('Z',0x01,0xD)
    ram_unit.map(ram,0,0x2fff)
    ram_unit.map(screen_dev,0x3000,0x30ff,remap=True)
    ram_unit.map(ram,0x3100,0xffff)
    _16bit=CPU(ram_unit)
    _16bit.run()

if __name__ == '__main__':
    process()
    # _16bit = CPU(ram)
    # _16bit.step()
    # _16bit.viewMemoryAt(0xffff-7)
    # print(hex(_16bit.getRegister(fp)))
    # print(hex(_16bit.getRegister(sp)))
    # print(hex(_16bit.stackFrameSize))
    # # _16bit.step()
    # _16bit.debug()
    # _16bit.step()
    # _16bit.debug()