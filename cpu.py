from memory import Memory
from memorymapper import MemoryMapper
from instr import Instruction
ip=0;acc=1;r1=2;r2=3;r3=4;r4=5;r5=6;r6=7;r7=8;r8=9;sp=10;fp=11
class CPU():
    def __init__(self,memory:MemoryMapper) -> None:
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
            sp:0xffff-1,
            fp:0xffff-1
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
            sp:'sp',
            fp:'fp'
        }
        self.stackFrameSize = 0
    
    def debug(self):
        for reg in self.registerNames:
            print(self.registerNames[reg]+":"+hex(self.registers[reg]))
        print("<================================>")

    def viewMemoryAt(self,address,n=8):
        res = hex(address)+':'
        for i in range(n):
            res+=" "+hex(self.memory.getUint8(address+i))
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
        # print(hex(self.registers[ip]))
        return instruction
    
    def fetch16(self):
        nextInstructionAddress = self.registers[ip]
        instruction = self.memory.getUint16(nextInstructionAddress)
        self.setRegister(ip,nextInstructionAddress+2)
        return instruction
    
    def push(self,value):
        spAddress = self.getRegister(sp)
        self.memory.setUint16(spAddress,value)
        self.setRegister(sp,spAddress-2)
        self.stackFrameSize+=2

    def pop(self):
        nextSpAddress = self.getRegister(sp)+2
        self.setRegister(sp,nextSpAddress)
        self.stackFrameSize-=2
        return self.memory.getUint16(nextSpAddress)
    
    def pushState(self):
        self.push(self.getRegister(r1))
        self.push(self.getRegister(r2))
        self.push(self.getRegister(r3))
        self.push(self.getRegister(r4))
        self.push(self.getRegister(r5))
        self.push(self.getRegister(r6))
        self.push(self.getRegister(r7))
        self.push(self.getRegister(r8))
        self.push(self.getRegister(ip))
        self.push(self.stackFrameSize+2)

        self.setRegister(fp,self.getRegister(sp))
        self.stackFrameSize = 0
    
    def popState(self):
        framePointerAddress = self.getRegister(fp)
        self.setRegister(sp,framePointerAddress)
        self.stackFrameSize = self.pop()
        stackFrameSize = self.stackFrameSize

        self.setRegister(ip,self.pop())
        self.setRegister(r8,self.pop())
        self.setRegister(r7,self.pop())
        self.setRegister(r6,self.pop())
        self.setRegister(r5,self.pop())
        self.setRegister(r4,self.pop())
        self.setRegister(r3,self.pop())
        self.setRegister(r2,self.pop())
        self.setRegister(r1,self.pop())
        
        nArgs = self.pop()
        for i in range(nArgs):
            self.pop()
        
        self.setRegister(fp,framePointerAddress+stackFrameSize)

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

        elif (instr == Instruction.PSH_LIT):
            value = self.fetch16()
            self.push(value)

        elif(instr == Instruction.PSH_REG):
            reg = self.fetch()
            self.push(self.getRegister(reg))
        
        elif(instr == Instruction.POP):
            reg = self.fetch()
            value = self.pop()
            self.setRegister(reg,value)

        elif(instr == Instruction.CAL_LIT):
            address = self.fetch16()
            self.pushState()
            self.setRegister(ip,address)
        
        elif (instr == Instruction.CAL_REG):
            reg = self.fetch()
            address = self.getRegister(reg)
            self.pushState()
            self.setRegister(ip,address)

        elif(instr == Instruction.RET):
            self.popState()

        elif(instr == Instruction.HLT):
            return True
        else:
            pass

        return False

    def step(self):
        instr = self.fetch()
        self.excute(instr)

    def run(self):
        i = 0
        while(True):
            i+=1
            # if (i>200):
            #     break
            if self.registers[ip] > 0xfff0:
                break
            self.step()

