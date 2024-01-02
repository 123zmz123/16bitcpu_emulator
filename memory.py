import array
class Memory():
    def __init__(self,sizeInbytes) -> None:
        self.raw_mem = array.array('B',[0]*sizeInbytes)
    
    def getUint8(self,address):
        return self.raw_mem[address]
        pass

    def getUint16(self,address):
        uint16_res = self.raw_mem[address]<<8 | self.raw_mem[address+1]
        return uint16_res
    
    def setUint16(self,address,value):
        value_h = ((value>>8) & 0xff)
        value_l = (value & 0xff)
        self.raw_mem[address]=value_h
        self.raw_mem[address+1]=value_l
    def __len__(self):
        return len(self.raw_mem)
    
if __name__ == '__main__':
    mem = Memory(16)
    mem.raw_mem[0]=0x01
    mem.raw_mem[1]=0x02
    mem.raw_mem[2]=0x14
    mem.setUint16(0,0x789a)
    print(hex(mem.raw_mem[0]))
    print(hex(mem.raw_mem[1]))
    print(len(mem))
    