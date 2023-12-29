from memory import Memory
from instr import Instruction
ip=0;acc=1;r1=2;r2=3;r3=4;r4=5;r5=6;r6=7;r7=8;r8=9
class CPU():
    def __init__(self,memory:Memory) -> None:
        self.memory = memory
        self.registers = {
            ip:0,
            acc:0,
            r1:0,
            r2:0,
            r3:0,
            r4:0,
            r5:0,
            r6:0,
            r7:0,
            r8:0,
        }
        self.registerNames = {
            ip:'ip',
            acc:'acc',
            r1:'r1',
            r2:'r2',
            r3:'r3',
            r4:'r4',
            r5:'r5',
            r6:'r6',
            r7:'r7',
            r8:'r8',
        }
    
    def debug(self):
        for reg in self.registerNames:
            print(self.registerNames[reg]+":"+hex(self.registers[reg]))
        print("<================================>")

    def viewMemoryAt(self,address):
        res = hex(address)+':'
        for i in range(8):
            res+=" "+hex(self.memory.raw_mem[address+i])
        print(res)

    def getRegister(self,name):
        #todo maybe we need support getUint16 feature
        return self.registers[name]

    def setRegister(self,name,value):
        #todo maybe we need support setUint16 feature
        self.registers[name]=value
    
    def fetch(self):
        nextInstructionAddress = self.registers[ip]
        instruction = self.memory.getUint8(nextInstructionAddress)
        self.setRegister(ip,nextInstructionAddress+1)
        return instruction
    
    def fetch16(self):
        nextInstructionAddress = self.registers[ip]
        instruction = self.memory.getUint16(nextInstructionAddress)
        self.setRegister(ip,nextInstructionAddress+2)
        return instruction

    def excute(self,instr):
        if(instr == Instruction.MOV_LIT_REG):
            literal = self.fetch16()
            reg = self.fetch()
            self.setRegister(reg,literal)

        elif(instr == Instruction.MOV_REG_REG):
            registerFrom = self.fetch()
            registerTo = self.fetch()
            value = self.getRegister(registerFrom)
            self.setRegister(registerTo,value)

        elif(instr == Instruction.MOV_REG_MEM):
            registerFrom = self.fetch()
            address = self.fetch16()
            value = self.getRegister(registerFrom)
            self.memory.setUint16(address,value)

        elif (instr == Instruction.MOV_MEM_REG):
            address = self.fetch16()
            registerTo = self.fetch()
            value = self.memory.getUint16(address)
            self.setRegister(registerTo,value)

        elif (instr == Instruction.ADD_REG_REG):
            r1 = self.fetch()
            r2 = self.fetch()
            r1_value = self.getRegister(r1)
            r2_value = self.getRegister(r2)
            self.setRegister(acc,r1_value+r2_value)

        elif (instr == Instruction.JMP_NOT_EQ):
            value = self.fetch16()
            address = self.fetch16()
            if (value != self.getRegister(acc)):
                self.setRegister(ip,address)
        else:
            pass

    def step(self):
        instr = self.fetch()
        self.excute(instr)


    
