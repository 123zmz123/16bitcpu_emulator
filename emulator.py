from memory import Memory
from cpu import CPU
from instr import Instruction
ip=0;acc=1;r1=2;r2=3;r3=4;r4=5;r5=6;r6=7;r7=8;r8=9;sp=10;fp=11
ram = Memory(256*256)
subroutineAddress = 0x3000
i = 0
ram.raw_mem[i]=Instruction.PSH_LIT
i+=1
ram.raw_mem[i]=0x33
i+=1
ram.raw_mem[i]=0x33
i+=1


ram.raw_mem[i]=Instruction.PSH_LIT
i+=1
ram.raw_mem[i]=0x22
i+=1
ram.raw_mem[i]=0x22
i+=1

ram.raw_mem[i]=Instruction.PSH_LIT
i+=1
ram.raw_mem[i]=0x11
i+=1
ram.raw_mem[i]=0x11
i+=1


ram.raw_mem[i]=Instruction.MOV_LIT_REG
i+=1
ram.raw_mem[i]=0x12
i+=1
ram.raw_mem[i]=0x34
i+=1
ram.raw_mem[i]=r1
i+=1


ram.raw_mem[i]=Instruction.MOV_LIT_REG
i+=1
ram.raw_mem[i]=0x56
i+=1
ram.raw_mem[i]=0x78
i+=1
ram.raw_mem[i]=r4
i+=1

ram.raw_mem[i] = Instruction.PSH_LIT
i+=1
ram.raw_mem[i]=0x00
i+=1
ram.raw_mem[i]=0x00
i+=1

ram.raw_mem[i]=Instruction.CAL_LIT
i+=1
ram.raw_mem[i] = (subroutineAddress & 0xff00)>>8
i+=1
ram.raw_mem[i]= (subroutineAddress & 0xff)
i+=1


ram.raw_mem[i] = Instruction.PSH_LIT;               i+=1
ram.raw_mem[i] =0x44                ;               i+=1
ram.raw_mem[i] =0x44                ;               i+=1


i = subroutineAddress
ram.raw_mem[i] = Instruction.PSH_LIT; i+=1
ram.raw_mem[i] = 0x01;  i+=1
ram.raw_mem[i] = 0x02;  i+=1

ram.raw_mem[i] = Instruction.PSH_LIT; i+=1
ram.raw_mem[i] = 0x03;  i+=1
ram.raw_mem[i] = 0x04;  i+=1

ram.raw_mem[i] = Instruction.PSH_LIT; i+=1
ram.raw_mem[i] = 0x05;  i+=1
ram.raw_mem[i] = 0x06;  i+=1


ram.raw_mem[i] = Instruction.MOV_LIT_REG;  i+=1
ram.raw_mem[i] = 0x07;  i+=1
ram.raw_mem[i] = 0x08;  i+=1
ram.raw_mem[i] =r1;  i+=1

ram.raw_mem[i] = Instruction.MOV_LIT_REG;  i+=1
ram.raw_mem[i] = 0x09;  i+=1
ram.raw_mem[i] = 0x0A;  i+=1
ram.raw_mem[i] =r8;  i+=1

ram.raw_mem[i]=Instruction.RET;i+=1


def process():
    _16bit=CPU(ram)
    while(True):
        cmd = input("command:")
        if (cmd == "s"):
            _16bit.step()
            _16bit.debug()
            _16bit.viewMemoryAt(0xffff-40,41)
        elif(cmd =='q'):
            break

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