from memory import Memory
from memorymapper import MemoryMapper
from screen_device import Screen
from cpu import CPU
from instr import Instruction
ip=0;acc=1;r1=2;r2=3;r3=4;r4=5;r5=6;r6=7;r7=8;r8=9;sp=10;fp=11
ram = Memory(256*256)
waitSubroutineAddress = 0x3110
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


    ram_unit.map(ram,0,0x2fff)
    ram_unit.map(screen_dev,0x3000,0x30ff,remap=True)
    ram_unit.map(ram,0x3100,0xffff)
    _16bit=CPU(ram_unit)
    _16bit.run()
    _16bit.debug()
def in_finite_screen_refresh():
    global i
    for index in range(256):
        writeCharToScreen("A",0x01,index)
    ram.raw_mem[i]=Instruction.PSH_LIT;i+=1
    ram.raw_mem[i]=0;i+=1
    ram.raw_mem[i]=0;i+=1

    ram.raw_mem[i]=Instruction.CAL_LIT;i+=1
    ram.raw_mem[i]=(waitSubroutineAddress&0xff00)>>8;i+=1
    ram.raw_mem[i]=(waitSubroutineAddress&0xff);i+=1
    for index in range(256):
        writeCharToScreen(".",0x01,index)

    ram.raw_mem[i]=Instruction.MOV_LIT_REG;i+=1
    ram.raw_mem[i]=0;i+=1
    ram.raw_mem[i]=0;i+=1
    ram.raw_mem[i]=ip;i+=1

    i = waitSubroutineAddress
    ram.raw_mem[i]=Instruction.MOV_LIT_REG;i+=1
    ram.raw_mem[i]=0;i+=1
    ram.raw_mem[i]=1;i+=1
    ram.raw_mem[i]=r1;i+=1

    ram.raw_mem[i]=Instruction.MOV_LIT_REG;i+=1
    ram.raw_mem[i]=0;i+=1
    ram.raw_mem[i]=0;i+=1
    ram.raw_mem[i]=acc;i+=1

    loopStart = i

    ram.raw_mem[i] = Instruction.ADD_REG_REG;i+=1
    ram.raw_mem[i]=r1;i+=1
    ram.raw_mem[i]=acc;i+=1

    ram.raw_mem[i]=Instruction.JMP_NOT_EQ;i+=1
    ram.raw_mem[i]=0xff;i+=1
    ram.raw_mem[i]=0xff;i+=1
    ram.raw_mem[i]=(loopStart & 0xff00)>>8;i+=1
    ram.raw_mem[i]=(loopStart & 0xff);i+=1

    ram.raw_mem[i]=Instruction.RET;i+=1
    pass

def test_MOV_REG_PTR_REG():
    global i
    i=0
    ram.raw_mem[i]= Instruction.MOV_LIT_REG;i+=1
    ram.raw_mem[i]=0x10;i+=1
    ram.raw_mem[i]=0x10;i+=1
    ram.raw_mem[i]=r1;i+=1

    ram.raw_mem[i]=Instruction.MOV_REG_PTR_REG;i+=1
    ram.raw_mem[i]=r1;i+=1
    ram.raw_mem[i]=r2;i+=1
    ram.raw_mem[i]=0xFF;i+1
    i=0x1010
    ram.raw_mem[i]=0x44;i+=1
    ram.raw_mem[i]=0x77;i+=1
    pass

def test_MOV_LIT_OFF_REG():
    global i
    i=0
    ram.raw_mem[i]=Instruction.MOV_LIT_REG;i+=1
    ram.raw_mem[i]=0x00;i+=1
    ram.raw_mem[i]=0x02;i+=1
    ram.raw_mem[i]=r1;i+=1

    ram.raw_mem[i]=Instruction.MOV_LIT_OFF_REG;i+=1
    ram.raw_mem[i]=0x10;i+=1
    ram.raw_mem[i]=0x10;i+=1
    ram.raw_mem[i]=r1;i+=1
    ram.raw_mem[i]=r2;i+=1
    ram.raw_mem[i]=0xFF;i+=1
    i = 0x1012
    ram.raw_mem[i]=0x13;i+=1
    ram.raw_mem[i]=0x14;i+=1
    pass

def test_ADD_LIT_REG():
    global i
    ram.raw_mem[i]=Instruction.ADD_LIT_REG;i+=1
    ram.raw_mem[i]=0x11;i+=1
    ram.raw_mem[i]=0x21;i+=1
    ram.raw_mem[i]=r2;i+=1
    ram.raw_mem[i]=0xFF;i+=1

def test_SUB_LIT_REG():
    global i
    ram.raw_mem[i]=Instruction.SUB_LIT_REG;i+=1
    ram.raw_mem[i]=0x1;i+=1
    ram.raw_mem[i]=0x1;i+=1
    ram.raw_mem[i]=r1;i+=1
    ram.raw_mem[i]=0xFF;i+=1

def test_SUB_REG_LIT():
    global i
    ram.raw_mem[i]=Instruction.SUB_REG_LIT;i+=1
    ram.raw_mem[i]=r1;i+=1
    ram.raw_mem[i]=0x02;i+=1
    ram.raw_mem[i]=0x03;i+=1
    ram.raw_mem[i]=0xFF;i+=1

if __name__ == '__main__':
    # in_finite_screen_refresh()
    test_SUB_REG_LIT()
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