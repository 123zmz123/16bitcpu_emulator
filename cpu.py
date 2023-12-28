from memory import Memory
from instr import Instruction

class CPU():
    def __init__(self,memory:Memory) -> None:
        self.memory = memory
        self.registers = {
            'ip':0,
            'acc':0,
            'r1':0,
            'r2':0,
            'r3':0,
            'r4':0,
            'r5':0,
            'r6':0,
            'r7':0,
            'r8':0,
        }
    
    def debug(self):
        for reg in self.registers:
            print(reg+":"+hex(self.registers[reg]))
        print("<================================>")

    def getRegister(self,name):
        #todo maybe we need support getUint16 feature
        return self.registers[name]

    def setRegister(self,name,value):
        #todo maybe we need support setUint16 feature
        self.registers[name]=value
    
    def fetch(self):
        nextInstructionAddress = self.registers['ip']
        instruction = self.memory.getUint8(nextInstructionAddress)
        self.setRegister('ip',nextInstructionAddress+1)
        return instruction
    
    def fetch16(self):
        nextInstructionAddress = self.registers['ip']
        instruction = self.memory.getUint16(nextInstructionAddress)
        self.setRegister('ip',nextInstructionAddress+2)
        return instruction

    def excute(self,instr):
        if (instr == Instruction.MOVE_LIT_R1):
            literal = self.fetch16()
            self.setRegister('r1',literal)
            return

        elif(instr == Instruction.MOVE_LIT_R2):
            literal = self.fetch16()
            self.setRegister('r2',literal)
            return

        elif(instr == Instruction.ADD_REG_REG):
            r1_idx = self.fetch()
            r2_idx = self.fetch()
            r_1 = 'r'+str(r1_idx)
            r_2 = 'r'+str(r2_idx)
            r1_val = self.registers[r_1]
            r2_val = self.registers[r_2]
            self.setRegister('acc',r1_val+r2_val)
            return
        else:
            pass
    def step(self):
        instr = self.fetch()
        self.excute(instr)


    
